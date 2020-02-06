from util import Player
import requests
​
BRYAN_TOKEN="64d8129bb04ced928d49f594740060746653ad9b"
MATT_TOKEN="14c573287422fb859d763daacf394c13ad6dcbc6"
SEAN_TOKEN="f7d185032deae45d2005b15029ebcb7d53c0c4df"
BLAINE_TOKEN="867bde1d09ebfad6c81fa9fa5bda855b3e16c3d6"
​
# API_URL = "https://quick-baboons.herokuapp.com"
API_URL = "http://localhost:6000"
LS_API_URL = "https://lambda-treasure-hunt.herokuapp.com"
​
# Load Player instances
players = []
​
requests_blaine = requests.Session()
requests_blaine.headers.update({
    "Authorization": BLAINE_TOKEN
})
# r = requests_blaine.get(API_URL+"/api/rooms/init")
# player_data = r.json()["player"]
# players.append(Player("Blaine", str(player_data['room_id']), requests_blaine))
​
requests_bryan = requests.Session()
requests_bryan.headers.update({
    "Authorization": BRYAN_TOKEN
})
# r = requests_bryan.get(API_URL+"/api/rooms/init")
# player_data = r.json()["player"]
# players.append(Player("Bryan", str(player_data['room_id']), requests_bryan))
​
requests_matt = requests.Session()
requests_matt.headers.update({
    "Authorization": MATT_TOKEN
})
r = requests_matt.get(API_URL+"/api/rooms/init")
player_data = r.json()["player"]
# players.append(Player("Matt", str(player_data['room_id']), requests_matt))

matt = Player("Matt", str(player_data['room_id']), requests_matt)
​
requests_sean = requests.Session()
requests_sean.headers.update({
    "Authorization": SEAN_TOKEN
})
# r = requests_sean.get(API_URL+"/api/rooms/init")
# player_data = r.json()["player"]
# players.append(Player("Sean", str(player_data['room_id']), requests_sean))
​
# FORMAT OF CUSTOM requests session
# res = requests_matt.get(API_URL+"/api/rooms/init")