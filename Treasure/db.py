from thesecrets import requests_matt, MATT_TOKEN, API_URL
import time, os, json

class Database:
    def __init__(self, name):
        self.name = name
        self.data = dict()

    # Load local player persistence or create if empty
    def load_db(self):
        player_data = None
        if f"{self.name}_data.json" not in os.listdir():
            data = None
            with open("user_data.json", "r") as user_json:
                data = json.load(user_json)
                data["name"] = self.name
            with open(f"{self.name}_data.json", "w") as player_json:
                json.dump(data, player_json)
                player_data = data
        else:
            with open(f"{self.name}_data.json", "r") as player_json:
                player_data = json.load(player_json)
        self.data = player_data


    def _read_db(self):
        pass


    def _update_db(self):
        with open(f"{self.name}_data.json", "w") as player_json:
            json.dump(self.data, player_json)


    def get_item(self, item):
        if item in self.data.keys():
            return self.data[item]
        else:
            raise Exception(f"{item} does not exist in the db")


    def set_item(self, key, value):
        self.data[key] = value
        self._update_db()