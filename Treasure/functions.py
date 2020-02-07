from classes import Graph, Queue
from thesecrets import API_URL, LS_API_URL
from miner import mine_coin
from cpu import CPU
from dijkstra import dijk_path
import requests, time, random

def sync_graph(g):
    """
    Syncs the local graph with the db
    """
    # Hit the /api/rooms/adlist endpoint and update the local graph with the returned adjacency list
    r = requests.get(API_URL+"/api/rooms/adlist")
    ad_list = r.json()

    # Add vertices
    for room_id in ad_list:
        # Add room_id as a vertex if not in g
        if room_id not in g.vertices:
            g.add_vertex(room_id)

    # Add edges
    for room_id in ad_list:
        neighbors = ad_list[room_id]
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            neighbor_direction = list(neighbor.keys())
            neighbor_direction = neighbor_direction[0]

            neighbor_id = neighbor[neighbor_direction]
            
            g.add_edge(room_id, str(neighbor_id), neighbor_direction)


def move_and_update_graph(player, direction, visited):
    """ 
    ONLY USE IF YOU NEED TO UPDATE THE DB
    Just moves the player and updates the visited set.
    """
    print(f"moving {direction}")
    # Save previous room to update graph after moving
    prev_room = player.cur_room

    payload = {'direction': direction}
    r = player.requests.post(API_URL+'/api/rooms/move', json=payload)
    res = r.json()
    print(res)
    # After moving:
    new_room_id = str(res['room_id'])
    print(f"Moved to room {new_room_id}")
    cooldown = res['cooldown'] + 1
    # Add room_id to visited set
    visited.add(new_room_id)
    # Add new vertex if new_room_id is not present in g.vertices
    if new_room_id not in g.vertices:
        g.add_vertex(new_room_id)
        # update the edges as well
        g.add_edge(prev_room, new_room_id, direction)
    # Update player.cur_room
    player.cur_room = new_room_id
    # Sleep for cooldown seconds
    print(f"Cooling down for {cooldown} seconds")
    time.sleep(cooldown)
    # --pick up items--
    if len(res['items']) > 0:
        pick_up_items(res["items"].split(','))


def find_nearest_unvisited(player, visited):
    """
    Used only to repopulate a db that has less than 500 rooms.
    """
    room_id = player.cur_room
    neighbors = g.get_neighbors(room_id)
    q = Queue()

    # FORMAT OF QUEUE: [ [directions], [room_ids] ]
    # Initialize queue
    for direction in neighbors:
        if neighbors[direction] == '-1':
            # Return to main calling function
            print('Found next unvisited room 1 move away.')
            return [direction]
        else:
            # [directions to new location, new room id]
            room_id = neighbors[direction]
            q.enqueue( [ [direction], [room_id] ] )

    # START SEARCH
    while q.size() > 0:
        directions, room_ids = q.dequeue()
        last_room_id = room_ids[-1]
        # Get neighbors
        neighbors = g.get_neighbors(last_room_id)
        neighbors_keys = list(neighbors.keys())
        random.shuffle(neighbors_keys)
        for direction in neighbors_keys:
            r_id = neighbors[direction]
            if r_id == '-1':
                directions.append(direction)
                print(f"Found next unvisited room {len(directions)} moves away.")
                return directions
            elif r_id not in room_ids:
                new_directions = list(directions)
                new_directions.append(direction)
                new_room_ids = list(room_ids)
                new_room_ids.append(r_id)
                q.enqueue([ new_directions, new_room_ids ])


item_counter = 0
def pick_up_items(arr):
    """
    Picks up an item
    """
    for item in arr[0:-1]:
        cooldown = 8
        # we don't want tiny treasure because it takes up space and we can't pick up more than 10
        # if item != 'tiny treasure' or item_counter < 8:
        if item != '':
            #pick up Item
            post_data = {"name": item}
            headers= {"Authorization": f"Token {MATT_TOKEN}" } #we need to put the token here
            r = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, json=post_data)
            print('response1', r)
            response = r.json()
            print('response', response)
            #set cooldown
            # cooldown = response["cooldown"]
            time.sleep(cooldown)
            
            #print errors if any
            if len(response["errors"]) > 0:
                print("can't pick up Item", item, response["errors"])
                #print error cooldown message
                print('error cooldown ' + str(response["cooldown"]) + ' seconds')
            else:
                # item_counter += 1 # if no errors, item was picked up
                #print normal cooldown message
                print('pick up item cooldown ' + str(response["cooldown"]) + ' seconds')
        else:
            print('ERROR: bad item: ', item)


def traverse_path(player, path):
    """
    Optimally traverses the path by using dash and fly when available.
    """
    for direction in path:
        payload = {'direction': direction}
        print(f"Moving {direction}")
        r = player.requests.post(API_URL+'/api/rooms/move', json=payload)
        res = r.json()
        print("response from hitting /move", res)
        # After moving:
        new_room_id = str(res['room_id'])
        print(f"Moved to room {new_room_id}")
        cooldown = res['cooldown'] + 0.5
        # Update player.cur_room
        player.cur_room = new_room_id
        # Sleep for cooldown seconds
        print(f"Cooling down for {cooldown} seconds")
        time.sleep(cooldown)
        # --pick up items--
        # if len(res['items']) > 0:
        #     pick_up_items(res["items"].split(','))


def go_to_shop(player):
    pass

def path_to_room_id(player, target_room_id, g):
    """
    Takes in a Player object and a target room id and returns the shortest path (using unweighted graph)
    """
    room_id = player.cur_room
    if room_id == target_room_id:
        return []
    # room_id = player.cur_room
    neighbors = g.get_neighbors(room_id)
    q = Queue()

    # FORMAT OF QUEUE: [ [directions], [room_ids] ]
    # Initialize queue
    for direction in neighbors:
        if neighbors[direction] == target_room_id:
            # Return to main calling function
            print(f'Found {target_room_id} 1 move away')
            print(directions)
            return [direction]
        else:
            # [directions to new location, new room id]
            room_id = neighbors[direction]
            q.enqueue( [ [direction], [room_id] ] )

    # START SEARCH
    while q.size() > 0:
        directions, room_ids = q.dequeue()
        last_room_id = room_ids[-1]
        # Get neighbors
        neighbors = g.get_neighbors(last_room_id)
        neighbors_keys = list(neighbors.keys())
        random.shuffle(neighbors_keys)
        for direction in neighbors_keys:
            r_id = neighbors[direction]
            if r_id == target_room_id:
                directions.append(direction)
                print(f'Found room {target_room_id} {len(directions)} moves away.')
                print(directions)
                return directions
            elif r_id not in room_ids:
                new_directions = list(directions)
                new_directions.append(direction)
                new_room_ids = list(room_ids)
                new_room_ids.append(r_id)
                q.enqueue([ new_directions, new_room_ids ])



def make_it_rain(player, player_token, g):
    """
    Mines coins until the end of time.
    """
    # Check to see if we know the mining room for player
    miner_room = player.db.get_item("miner_room")

    if miner_room == "":
        # Recall to origin
        headers = {
            "Authorization": f"Token {player_token}",
            "Content-Type": "application/json"
        }
        r = requests.post(LS_API_URL+'/api/adv/recall', headers=headers)
        res = r.json()
        print(f"Recalled to origin, cooling down for {res['cooldown']} seconds.")
        time.sleep(res['cooldown'])
        player.cur_room = '0'

        # Go to wishing well
        # path_to_wishing_well = dijk_path(player.cur_room, '55')
        path_to_wishing_well = path_to_room_id(player, '55', g)
        traverse_path(player, path_to_wishing_well)

        # Examine the wishing well
        post_body = { "name": "well" }
        r = requests.post(LS_API_URL+'/api/adv/examine/', json=post_body, headers=headers)
        res = r.json()
        secret_room_binary = res['description']
        secret_room_binary = secret_room_binary[41:]
        secret_room_binary = secret_room_binary.split('\n')

        # Parse the returned binary and set the mining_room_id to player.mining_room
        cpu = CPU()
        cpu.load(secret_room_binary)
        miner_room = cpu.run()
        player.db.set_item("miner_room", miner_room)
    
    # Traverse to the mining room we just found
    print('⛏ Moving to the miner room! ⛏')
    path_to_mining_room = path_to_room_id(player, player.db.get_item("miner_room"), g)
    # path_to_mining_room = dijk_path(player.cur_room, player.mining_room)
    traverse_path(player, path_to_mining_room)

    # Mine until we find a coin
    mined = False
    while not mined:
        mined = mine_coin(player_token)
    player.db.set_item("miner_room", "")
