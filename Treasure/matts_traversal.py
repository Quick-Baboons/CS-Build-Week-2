from classes import Player, Graph
from thesecrets import requests_matt, MATT_TOKEN, API_URL
from functions import sync_graph, make_it_rain
import time, requests, pdb, random, os, json

# === Initialize local script state ===
# Initialize player
r = requests_matt.get(API_URL+"/api/rooms/init")
player_data = r.json()["player"]
matt = Player("Matt", str(player_data['room_id']), requests_matt)
print('Running matts_traversal.py script...')

# Sleep to clear cooldown from init
time.sleep(1)

# Initialize the local graph
g = Graph()
sync_graph(g)
        

# === Do stuff here ===
# Try mining a coin
while True:
   make_it_rain(matt, MATT_TOKEN, g)

# headers = {}
# r = requests.post(API_URL+'/api/rooms/move', json={'direction': 's'})
# res = r.json()
# print('res', res)