import hashlib

import sys
from uuid import uuid4
import requests
import os
# from dotenv import load_dotenv
# load_dotenv()
import time

from timeit import default_timer as timer
import random


def proof_of_work(last_proof, difficulty):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """
    start = timer()

    print("Searching for next proof")
    proof = 0
    #  TODO: Your code here
    while valid_proof(last_proof,proof,difficulty) is False:
        proof = random.randint(1,99999999999)

    return proof

def valid_proof(last_proof, current_guess, difficulty):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    # TODO: Your code here!
    current_combo = f'{last_proof}{current_guess}'.encode()
    combo_hash = hashlib.sha256(current_combo).hexdigest()
    return combo_hash[:difficulty] == "0" * difficulty


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    # f = open("my_id.txt", "r")
    # id = f.read()
    # print("ID is", id)
    # f.close()
    headers = {
    'Authorization': 'Token d3f3a0266824458c28f1e36c817636085dcc3106',
    'Content-Type': 'application/json'
}

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/bc/last_proof", headers=headers)
        data = r.json()
        time.sleep(data["cooldown"])
        print(data)
        
        new_proof = proof_of_work(data.get('proof'),data["difficulty"])
        post_data = {"proof": new_proof}

        r2 = requests.post(url=node + "/bc/mine", json=post_data, headers=headers).json()
        time.sleep(r2["cooldown"])