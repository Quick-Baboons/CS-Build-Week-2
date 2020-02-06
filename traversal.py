from util import Player, Graph, Queue, Stack
from thesecrets import bryan, BRYAN_TOKEN, API_URL
import time, requests, pdb, random
import multiprocessing as mp

OPPOSITE_DIRECTION = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# === Initialize local script state ===

# Initialize the local graph
def sync_graph(g):
    # Hit the /api/rooms/adlist endpoint and update the local graph with the returned adjacency list
    r = bryan.requests.get(API_URL+"/api/rooms/adlist")
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

# First graph sync
g = Graph()
sync_graph(g)
        
# === Find nearest unvisited room ===
# Main function
def find_nearest_unvisited(player, visited):
    room_id = player.cur_room
    neighbors = g.get_neighbors(room_id)
    q = Queue()

    # FORMAT OF QUEUE: [ [directions], [room_ids] ]
    # Initialize queue
    for direction in neighbors:
        if neighbors[direction] == '-1':
            # Return to main calling function
            print(f'Found next unvisited room 1 move away.')
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
                print(f'Found next unvisited room {len(directions)} moves away.')
                return directions
            elif r_id not in room_ids:
                new_directions = list(directions)
                new_directions.append(direction)
                new_room_ids = list(room_ids)
                new_room_ids.append(r_id)
                q.enqueue([ new_directions, new_room_ids ])

item_counter = 0
def pick_up_items(arr):
    for item in arr:
        cooldown = 0
        # we don't want tiny treasure because it takes up space and we can't pick up more than 10
        if item != 'tiny treasure' or item_counter < 8:
            #pick up Item
            post_data = {"name": item}
            headers= {"Authorization": "Token ***********************" } #we need to put the token here
            r = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', data=post_data, headers=headers)
            response = r.json()
            #set cooldown
            cooldown = response["cooldown"]
            print('response', response)
            #print errors if any
            if len(response["errors"]) > 0:
                print("can't pick up Item", item, response["errors"])
                #print error cooldown message
                print('error cooldown ' + str(response["cooldown"]) + ' seconds')
            else:
                item_counter += 1 # if no errors, item was picked up
                #print normal cooldown message
                print('pick up item cooldown ' + str(response["cooldown"]) + ' seconds')
        else:
            print('ERROR: item was tiny treasure or our pack is full')
        
        #cooldown
        time.sleep(cooldown)
        
def move(player, direction, visited):
    """ 
    Just moves the player and updates the visited set
    """
    print(f"moving {direction}")
    # Save previous room to update graph after moving
    prev_room = player.cur_room

    payload = {'direction': direction}
    r = player.requests.post(API_URL+'/api/rooms/move', json=payload)
    res = r.json()
    # After moving:
    new_room_id = str(res['room_id'])
    print(f"Moved to room {new_room_id}")
    cooldown = res['cooldown']
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
    # if len(res["items"]) > 0:
        # pick_up_items(res["items"])


visited = {room for room in g.vertices}
# Main script loop which calls find_nearest_unvisited()
player = bryan
time.sleep(1)
# FULL TRAVERSAL
while len(visited) < 500:
    path = find_nearest_unvisited(player, visited) # path is a list of directions
    print(f"Found shortest path \n {path}")
    for direction in path:
        move(player, direction, visited)

# print('currom', player.cur_room)
# target = g.vertices[467]
# for vertex in g.vertices:
#     print(vertex)
# path = g.bfs(player.cur_room, 467)
# print('path: ', path)
# Re-sync local graph/vertices with db
    # g = Graph()
    # sync_graph(g)
    # visited = {room for room in g.vertices}