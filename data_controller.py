import json


class DataController:
    def __init__(self):
        self.personal = {}
        self.ships = {}

    def load_personal_data(self):
        with open('data/personal.json', 'r') as f:
            data = json.load(f)
        self.personal = data

    def dump_personal_data(self):
        with open('data/personal.json', 'w') as f:
            json.dump(self.personal, f)

    def load_ships_data(self):
        with open('data/ships.json', 'r') as f:
            data = json.load(f)
        self.ships = data

    def dump_ships_data(self):
        with open('data/ships.json', 'w') as f:
            json.dump(self.ships, f)
