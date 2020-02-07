from db import Database

OPPOSITE_DIRECTION = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

UNIQUE_ROOMS = {
    'wish': {  # Go here to mine lambda coins
        'full_name': 'Wishing Well',
        'room_id': '55'
    },
    'shop': {  # Sell items for gold here
        'full_name': 'Shop',
        'room_id': '1'
    },
    'origin': {  # Starting room
        'full_name': 'A brightly lit room',
        'room_id': '0'
    },
    'holloway': {  # Shrine to gain FLY ability
        'full_name': 'The Peak of Mt. Holloway',
        'room_id': '22'
    },
    "grave": {  # Shrine to gain CARRY ability to put items on a ghost
        'full_name': 'Glasowyn\'s Grave',
        'room_id': '499'
    },
    "linh": {  # Shrine pray to get DASH
        'full_name': 'Linh\'s Shrine',
        'room_id': '461'
    },
    "pirate": {  # Name Changer, gain PRAY & MINE ability
        'full_name': 'Pirate Ry\'s',
        'room_id': '467'
    },
    "sandofsky": {  # Shrine to gain RECALL ability
        'full_name': 'Sandofsky\'s Sanctum',
        'room_id': '492'
    },
    'fully': {  # Shrine to gain WARP ability to warp to underworld
        'full_name': 'Fully Shrine',
        'room_id': '374'
    },
    "aaron": {  # Not a shrine, Herin exists knowledge gathered by Arron of Web19/CS21
        'full_name': 'Arron\'s Athenaeum',
        'room_id': '486'
    },
    'trans': {  # Spend coins to make new equipment
        'full_name': 'The Transmogriphier',
        'room_id': '495'
    }
}


class Player:
    """
    Holds the player state necessary for the script
    """

    def __init__(self, name, cur_room, requests_session):
        self.name = name.lower()
        self.cur_room = cur_room
        self.requests = requests_session
        self.db = Database(self.name)
        self.db.load_db()


class Graph:
    """
    Represent a graph as a dictionary of vertices mapping labels to edges.
    """

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {}

    def add_edge(self, v1, v2, direction):
        """
        Add a directed edge to the graph.
        """
        # if v1 in self.vertices and v2 in self.vertices:
        if v1 != '-1':
            self.vertices[v1][direction] = v2
        if v2 != '-1':
            self.vertices[v2][OPPOSITE_DIRECTION[direction]] = v1
        # else:
        #     raise IndexError("One or both of the vertices does not exist")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise IndexError("Vertex does not exist")


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)
