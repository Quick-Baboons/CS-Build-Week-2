# from Treasure.thesecrets import API_URL

from classes import OPPOSITE_DIRECTION

from thesecrets import API_URL
import requests
import math



class Node:
  def __init__(self, val, priority):
    self.val = val
    self.priority = priority



class PriorityQueue:
  def __init__(self):
    self.values = []

  def enqueue(self, val, priority):
    new_node = Node(val, priority)

    self.values.append(new_node)
  

    current_idx = len(self.values) - 1
    parent_idx = math.floor( (current_idx - 1 ) /2)

    while parent_idx >= 0 and self.values[parent_idx].priority > self.values[current_idx].priority:

      parent_node = self.values[parent_idx]
      self.values[parent_idx] = self.values[current_idx]
      self.values[current_idx] = parent_node

      current_idx = parent_idx
      parent_idx = math.floor( (parent_idx - 1) / 2)

  def dequeue(self):

    if len(self.values) == 0: return IndexError("No values to dequeue")
    elif len(self.values) == 1: return self.values.pop()


    def higher_priority_idx(idx1, idx2):
      if idx2 < 0 or idx2 >= len(self.values):
        if idx1 < 0 or idx1 > len(self.values): return -1
        elif 0 <= idx1 <= len(self.values): return idx1

      elif self.values[idx1].priority < self.values[idx2].priority: return idx1  
      else: return idx2

    dequeued = self.values.pop(0)
    temp = self.values[0]

    self.values[0] = self.values[-1]
    self.values[-1] = temp



    current_idx = 0

    child_idx = higher_priority_idx(current_idx * 2 + 1, current_idx * 2 + 2)

    while child_idx < len(self.values) and self.values[child_idx].priority < self.values[current_idx].priority:
      child_node = self.values[child_idx]
      self.values[child_idx] = self.values[current_idx]
      self.values[current_idx] = child_node

      current_idx = child_idx
      child_idx = higher_priority_idx(child_idx * 2 + 1, child_idx*2 + 2)
      if child_idx == -1: break

    return dequeued
















class WeightedGraph:
  def __init__(self):
    self.adjacency_list = {}

  def add_vertex(self, vertex):
    if vertex not in self.adjacency_list: self.adjacency_list[vertex] = []

  def add_edge(self, v1, v2, weight, direction):

    if v1 and v2 in self.adjacency_list:

      for room_data in self.adjacency_list[v1]:
          if room_data['v'] == v2:
              return
      for room_data in self.adjacency_list[v2]:
          if room_data['v'] == v1:
              return


      self.adjacency_list[v1].append({'v':v2, 'weight':weight, 'direction':direction})
      self.adjacency_list[v2].append({'v':v1, 'weight':weight, 'direction':OPPOSITE_DIRECTION[direction]})
    else: return KeyError("One of the vertices are invalid")

  def dijkstra(self, start, finish):
    # nodes grabs the node with the smallest distance from the start
    # distances_from_start keeps track of how far from start each vertex is
    # previous keeps track of the previous node (smallest path)


    
    # val = room
    # priority = weight
    # direction = direction

    nodes = PriorityQueue()
    distances_from_start = {}
    previous_vertices = {}
    directions = []

    # Build inital state
    for vertex in self.adjacency_list:
      if vertex == start:
        nodes.enqueue(vertex, 0)
        distances_from_start[vertex] = 0 
      else:
        nodes.enqueue(vertex, math.inf)
        distances_from_start[vertex] = math.inf
      previous_vertices[vertex] = None


    # While there are still values in the priority queue
    while len(nodes.values) > 0:

      # Grab room with the smallest distance from start
      current_node = nodes.dequeue().val


      # If that node is finish, we've found the shortest path
      if current_node == finish:

        current_vertex = finish
        direction = previous_vertices[finish][1]
        path = []
        while current_vertex is not None and distances_from_start[current_vertex] is not None:
          path.append(direction)
          try:
            current_vertex = previous_vertices[current_vertex][0]
            direction = previous_vertices[current_vertex][1]
          except: return path[::-1]


        return path[::-1]


      # Find the neighbors of current_node
      # For each neighbor, calculate distance from A.
      # If distance from A is shorter than the recorded distance on distances_from_start
        # Update distances_from_start, previous_vertices and add it to the queue for future processing
      for neighbor in self.adjacency_list[current_node]:
        new_distance = distances_from_start[current_node] + neighbor['weight']
        if new_distance == distances_from_start[neighbor['v']]: 
          distances_from_start[neighbor['v']] = new_distance
          previous_vertices[neighbor['v']] = [current_node, neighbor['direction']] 
          nodes.enqueue(neighbor['v'], new_distance)

        if new_distance < distances_from_start[neighbor['v']]: 
          distances_from_start[neighbor['v']] = new_distance
          previous_vertices[neighbor['v']] = [current_node, neighbor['direction']] 
          nodes.enqueue(neighbor['v'], new_distance)


    

    








r = requests.get(API_URL+"/api/rooms/weighted")
res_data = r.json()



wg = WeightedGraph()


# Add rooms to adlist
for key in res_data:
    wg.add_vertex(key)




# Add all the traps first
for current_room in res_data:
    for direction_data in res_data[current_room]:
        weight = direction_data['weight']
        if weight == 30: 
            next_room = None
            direction = None
            for data in direction_data:
                if data != 'weight':
                    next_room = direction_data[data]
                    direction = data
            wg.add_edge(str(current_room), str(next_room), weight, direction)        



# add the rest
for current_room in res_data:
    for direction_data in res_data[current_room]:
        weight = direction_data['weight']
        if weight == 30: 
            next_room = None
            direction = None
            for data in direction_data:
                if data != 'weight':
                    next_room = direction_data[data]
                    direction = data
            wg.add_edge(str(current_room), str(next_room), weight, direction)    


# add everything
for current_room in res_data:
    for direction_data in res_data[current_room]:
        weight = direction_data['weight']
        if weight == 7.5: 
            next_room = None
            direction = None
            for data in direction_data:
                if data != 'weight':
                    next_room = direction_data[data]
                    direction = data
            wg.add_edge(str(current_room), str(next_room), weight, direction)  






def dijk_path(start, end):
  directions = wg.dijkstra(start, end)
  print("NUM OF DIRECTIONS", len(directions))
  print(directions)
  return directions




def test_dijk(start, end):
  directions = wg.dijkstra(start, end)
  # tests
  current_location = start
  current_location_data = wg.adjacency_list[start]


  for direction in directions: 
      for direction_data in current_location_data:
          if direction_data['direction'] == direction:
              current_location = direction_data['v']
              current_location_data = wg.adjacency_list[direction_data['v']]
              break

  return  {"Start:":start,"End":end, "directions":directions}

