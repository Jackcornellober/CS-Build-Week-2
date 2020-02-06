import requests
import os
import json
import random
# from dotenv import load_dotenv
# load_dotenv()
from util import Graph, add_explored
from threading import Timer
import time

headers = {
    'Authorization': 'Token 519bde8af1b66841d8183adcb62619787b1a198c',
    'Content-Type': 'application/json'
}

# ----------------- BUILD WORLD FROM DB --------------- #
world_graph = Graph()

full_rooms_array = requests.get(
    'https://bw2rooms.herokuapp.com/api/room/getAllRooms').json()

for i in full_rooms_array:
    world_graph.add_vertex(i["room_id"], i["title"], i["description"], i["coordinates"],
                           i["elevation"], i["terrain"], i["items"], i["exits"], i["messages"])

# print(world_graph.vertices[1])
# ----------------- BUILD WORLD FROM DB --------------- #

# ************ ALL PURPOSE MOVEMENT CODE BELOW ****************************************


def all_purpose_movement(last_room_id_list, destination, pray):

    def move():
        last_room_id = last_room_id_list.pop(0)
        path = world_graph.walk_to_room(last_room_id, destination.pop(0))

        print(path)
        modified_path = []
        for index, i in enumerate(path):
            if index < len(path) - 1:
                current = i
                after = path[index+1]
                for q in world_graph.vertices[current]["exits"]:
                    if world_graph.vertices[current]["exits"][q] == after:
                        modified_path.append(q)
        while len(modified_path) > 0:
            bfsdir = modified_path.pop(0)
            print('about to move in this direction: ', bfsdir, " to: ",
                  world_graph.vertices[last_room_id]["exits"][bfsdir])
            if world_graph.vertices[last_room_id]["exits"][bfsdir] != '?':
                payloads = {"direction": bfsdir, "next_room_id": str(
                    world_graph.vertices[last_room_id]["exits"][bfsdir])}
            else:
                payloads = {"direction": bfsdir}
            response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                     data=json.dumps(payloads), headers=headers).json()
            print(response)
            cooldown = response["cooldown"]
            print("cooldown: ", cooldown)
            time.sleep(cooldown + .2)
            last_room_id = response["room_id"]

    # weight = 0

    if pray is True:
        prayed = 0
        while prayed < 4:
            prayed += 1
            move()

        #  *********** AUTO-PRAYER CODE BELOW ******************
        prayer_response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/', headers=headers).json()
        cooldown = prayer_response["cooldown"]
        print(prayer_response)
        print("cooldown: ", cooldown)
        time.sleep(cooldown + .2)

    else:
        move()

        #  *********** TREASURE GATHERING CODE BELOW ******************
        # if len(response["items"]) > 0 and weight >= 8:
        #     print('too heavy')
        # if len(response["items"]) > 0 and weight < 8:
        #     treasure_data = '{"name":"treasure"}'
        #     treasure_response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=treasure_data).json()
        #     cooldown = treasure_response["cooldown"]
        #     print(treasure_response)
        #     print("cooldown: ", cooldown)
        #     time.sleep(cooldown + .2)


# def dash(start,end):
#     next_room_array = world_graph.walk_to_room(start,end)
#     next_room_array.pop(0)
#     print(next_room_array, "next room array")
#     next_room_ids = str(next_room_array.pop(0))
#     for i in next_room_array:
#         next_room_ids = next_room_ids + "," + str(i)
#     print(next_room_ids)
#     data = {"direction":"n", "num_rooms":str(len(next_room_array)), "next_room_ids":next_room_ids}
#     response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/dash/', headers=headers, data=json.dumps(data)).json()
#     print(response)

# dash(499,242)

# rooms of interest: 498 - Sandofsky (recall) ||| 486 - unknown ||| 55 - wishing well |||

# last_room_id_list = [0]

# destination = [random.randint(300,500)]

##### --------------- AUTO TREASURE FIND/SELL BELOW -------------------- #####

def collect_treasure():

    def move_to_shop():
        response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/recall/', headers=headers).json()
        print('recalling to room 0')
        cooldown = response["cooldown"]
        time.sleep(cooldown + .2)
        data = '{"direction":"w", "next_room_id":"1"}'
        response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', data=data, headers=headers).json()
        print('walking from room 0 to the shop, about to start selling')
        cooldown = response["cooldown"]
        time.sleep(cooldown + .2)

    def sell_treasure():
        status_response = requests.post(
            'https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers).json()
        sell_times = len(status_response["inventory"])
        data = '{"name":"treasure", "confirm":"yes"}'
        cooldown = status_response["cooldown"]
        time.sleep(cooldown + .2)
        print(f"We have {sell_times} items to sell")
        if sell_times > 0:
            for x in range(sell_times):
                response = requests.post(
                    'https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data).json()
                print(response)
                cooldown = response["cooldown"]
                time.sleep(cooldown + .2)
        else:
            print("You have nothing to sell")

    # def pickup_item():

    move_to_shop()
    sell_treasure()

    while True:
        weight = 0
        length = 0
        while length < 38:
            last_room_id_list = [1]
            destination = random.randint(100, 499)
            last_room_id = last_room_id_list.pop(0)
            path1 = world_graph.walk_to_room(last_room_id, destination)

            last_room_id_list2 = [destination]
            destination2 = random.randint(100, 499)
            last_room_id2 = last_room_id_list2.pop(0)
            path2 = world_graph.walk_to_room(last_room_id2, destination2)
            path = path1 + path2[1:]

            length = len(path)
        print(path1)
        print(path2)
        print(path)

        modified_path = []
        for index, i in enumerate(path):
            if index < len(path) - 1:
                current = i
                after = path[index+1]
                for q in world_graph.vertices[current]["exits"]:
                    if world_graph.vertices[current]["exits"][q] == after:
                        modified_path.append(q)
        while len(modified_path) > 0 and weight < 9:
            bfsdir = modified_path.pop(0)
            print('about to move in this direction: ', bfsdir, " to: ",
                  world_graph.vertices[last_room_id]["exits"][bfsdir])
            payloads = {"direction": bfsdir, "next_room_id": str(
                world_graph.vertices[last_room_id]["exits"][bfsdir])}
            response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/',
                                     data=json.dumps(payloads), headers=headers).json()
            cooldown = response["cooldown"]
            print(response)
            print("cooldown: ", cooldown)
            time.sleep(cooldown + .2)
            last_room_id = response["room_id"]

            if len(response["items"]) > 0 and weight >= 9:
                print('too heavy')
            if len(response["items"]) > 0 and weight < 9:
                treasure_data = '{"name":"treasure"}'
                treasure_response = requests.post(
                    'https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=treasure_data).json()
                cooldown = treasure_response["cooldown"]
                print(treasure_response)
                print("cooldown: ", cooldown)
                time.sleep(cooldown + .2)
                weight += 1

        move_to_shop()
        sell_treasure()


# last_room_id_list = [146]
# destination = [55]
# all_purpose_movement(last_room_id_list, destination, False)
collect_treasure()
