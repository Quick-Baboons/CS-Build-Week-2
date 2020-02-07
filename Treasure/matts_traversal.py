from classes import Player, Graph
from thesecrets import requests_matt, MATT_TOKEN, API_URL
from functions import sync_graph, make_it_rain
import time, requests, pdb, random

OPPOSITE_DIRECTION = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}
UNIQUE_ROOMS = { 
   'wish':{  # Go here to mine lambda coins
      'full_name': 'Wishing Well',
      'room_id':'55'
   },
   'shop':{ # Sell items for gold here
      'full_name': 'Shop',
      'room_id':'1'
   },
   'origin':{  # Starting room
      'full_name': 'A brightly lit room',
      'room_id':'0'
   },
   'holloway':{  # Shrine to gain FLY ability; 
      'full_name': 'The Peak of Mt. Holloway',
      'room_id':'22'
   },
   "grave":{ # Shrine to gain CARRY ability to put items on a ghost; DONE
      'full_name': 'Glasowyn\'s Grave',
      'room_id':'499'
   },
   "linh":{ # Shrine pray to get DASH, DONE
      'full_name': 'Linh\'s Shrine',
      'room_id':'461'
   },
   "pirate":{ # Name Changer, gain PRAY & MINE ability; DONE
      'full_name': 'Pirate Ry\'s',
      'room_id':'467'
   },
   "sandofsky":{ # Shrine to gain RECALL ability; DONE
      'full_name': 'Sandofsky\'s Sanctum',
      'room_id':'492'
   },
   'fully':{ # Shrine to gain WARP ability to warp to underworld;  DONE
      'full_name': 'Fully Shrine',
      'room_id':'374'
   },
   "aaron":{ # Not a shrine, Herin exists knowledge gathered by Arron of Web19/CS21
      'full_name': 'Arron\'s Athenaeum',
      'room_id':'486'
   },
   'trans':{ # Spend coins to make new equipment
      'full_name': 'The Transmogriphier',
      'room_id':'495'
   }
}

# === Initialize local script state ===
# Initialize player
r = requests_matt.get(API_URL+"/api/rooms/init")
player_data = r.json()["player"]
matt = Player("Matt", str(player_data['room_id']), requests_matt)
# Sleep to clear cooldown from init
time.sleep(1.5)

# Initialize the local graph
g = Graph()
sync_graph(g)
        

# Navigate to Shop
# path = path_to_room_id(player, UNIQUE_ROOMS['wish']['room_id'])
# path = path_to_room_id(player, '291')
# print(path)
# for direction in path:
#     move(player, direction, visited)

# Try mining a coin
while True:
   make_it_rain(matt, MATT_TOKEN, g)

# headers = {}
# r = requests.post(API_URL+'/api/rooms/move', json={'direction': 's'})
# res = r.json()
# print('res', res)