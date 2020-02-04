import requests
import os
# from dotenv import load_dotenv
# load_dotenv()
from util import Graph, add_explored
from threading import Timer

headers = {
    'Authorization': 'Token d3f3a0266824458c28f1e36c817636085dcc3106',
    'Content-Type': 'application/json',
}

world_graph = Graph()

explored_rooms = set()

last_room = 0

world_graph.add_vertex(0,  "A brightly lit room",  "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.",
                       "(60,60)",  0,  "NORMAL",  [],  ['?', '?', '?', '?'], ["You have walked south."])

# while len(explored_rooms) < 500:

#     direction = response[""]

#     data = {"direction":direction}

#     response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)

#     exits = response["exits"]

#     if response["room_id"] not in explored_rooms:
#         world_graph.add_vertex(response["room_id"],response["title"],response["description"],response["coordinates"],response["elevation"],response["terrain"],response["items"],exits,response["messages"])

#     cooldown = response["cooldown"]

#     r = Timer(cooldown + 1, add_explored, (explored_rooms,response["room_id"]))

#     last_room = response["room_id"]

# Once done looping, add everything to database

print(world_graph.vertices[0]["exits"])


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
