import requests
import os
import json
# from dotenv import load_dotenv
# load_dotenv()
from util import Graph, add_explored
from threading import Timer
import time

headers = {
'Authorization': 'Token d3f3a0266824458c28f1e36c817636085dcc3106',
'Content-Type': 'application/json'
}

node_headers = {
'Content-Type': 'application/json'
}

world_graph = Graph()

explored_rooms = set()


last_room_id = 0
world_graph.add_vertex(0,  "A brightly lit room",  "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.",  "(60,60)",  0,  "NORMAL",  [],  {'n':'?','e':'?','s':'?','w':'?'}, ["You have walked south."])
{explored_rooms.add(0)}
exits = {'n':'?','e':'?','s':'?','w':'?'}
direction = 's'

dir_reverse = {"n":"s","s":"n","e":"w","w":"e"}

while len(explored_rooms) < 500:

    contains_unexplored = False
    for i in exits:
        if exits[i] == '?':
            contains_unexplored = True
            direction = i
    if contains_unexplored is True:
        payloads = {"direction": direction}
        response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', data=json.dumps(payloads), headers=headers).json()
        print(response)
        exits = {}
        for d in response["exits"]:
            exits[d] = '?'
    
        exits[dir_reverse[direction]] = last_room_id
        
    
        if response["room_id"] not in explored_rooms:
            world_graph.add_vertex(response["room_id"],response["title"],response["description"],response["coordinates"],response["elevation"],response["terrain"],response ["items"],exits,response["messages"])
        
        world_graph.add_edge(last_room_id, direction, response["room_id"])
    
        cooldown = response["cooldown"]
        time.sleep(cooldown + 1)
        explored_rooms.add(response["room_id"])
        # r = Timer(cooldown + 1, add_explored, (explored_rooms,response["room_id"]))
        # r.start()
        last_room_id = response["room_id"]
    else:
        path = world_graph.unexplored_search(last_room_id)
        modified_path = []
        for index,i in enumerate(path):
            if index < len(path) - 1:
                current = i
                after = path[index+1]
                
                for q in world_graph.vertices[current]["exits"]:
                    if world_graph.vertices[current]["exits"][q] == after:
                        modified_path.append(q)
        
        while len(modified_path) > 0:
            bfsdir = modified_path.pop(0)
            print('about to move in this direction: ', bfsdir, " to: ", world_graph.vertices[last_room_id]["exits"][bfsdir])
            if world_graph.vertices[last_room_id]["exits"][bfsdir] != '?':
                payloads = {"direction": bfsdir, "next_room_id": str(world_graph.vertices[last_room_id]["exits"][bfsdir])}
                print('wise explorer activated, payload: ', payloads)
            else:
                payloads = {"direction": bfsdir}

            response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', data=json.dumps(payloads), headers=headers).json()
            print(response)
            cooldown = response["cooldown"]
            time.sleep(cooldown + 1)
            explored_rooms.add(response["room_id"])
            # r = Timer(cooldown + 1, add_explored, (explored_rooms,response["room_id"]))
            # r.start()
            last_room_id = response["room_id"]
        exits = world_graph.vertices[response["room_id"]]["exits"]

for i in world_graph.vertices:    
    post_room = requests.post('https://bw2rooms.herokuapp.com/api/room/addRoom', data=json.dumps(world_graph.vertices[i]),headers=node_headers).json()
    print(post_room)




# STEPS TO COMPLETION

# 1. Create and initialize graph with room 0    √

# 2. We need to move through the map and create a database of all the rooms
# ----- Save each room to our database
# ----- pass room_id to previous visited room as an edge
# ----- Possible Solution ----
# ------- Store previous room_id locally
# ------- Move in a direction to connected room
# ------- Store direction moved locally
# ------- Get new room_id from response once moved.
# ------- Call function that passes our previous room_id, new room_id, and direction
# ------- Function adds our new room_id as an edge to the previous room based on the direction we moved

# -- At this point we should have a database with a completed map. We can now use the wise-explorer ability to traverse that map faster.

# -- We now need to traverse the map picking up items and selling them for gold until we are at 1000 gold.

# 3. Create a BFT search for getting to the shop.

# 4. Create a function for picking up items

# 5. Create a function that checks our encumbrance to our strength
# ----- If they are close, trigger the function to get back to the shop
# ----- Sell the items at the shop to acquire gold
# ----- ??? Restart the traversal from the shop or go back to the last room we were at ???

# -- We need to keep looping through this process until we reach 1000 gold. Once we have 1000 gold we can begin the last section of the solution

# 6. Locate the name changer
# ----- Unknown if this is in a single spot or moves around the map
# ----- Also unknown if you need 1000 gold to even find the name changer
# ----- We may be able to test both of these possibilities. When we save the map to our database we can look through the data to see if the name changer is visible and what room it is in.
# ----- We can then build a check into our traversal to see if the name changer remains in the same spot.
# ----- If this is the case our locate name changer traversal can go straight to that room_id. Otherwise we need to traverse the whole map till we find the name changer
