import json
import os
import hashlib
from datetime import datetime

BLOCKCHAIN_FILE = "blockchain/blockchain.json"

def calculate_block_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def store_hash(evidence_id, hash_value):
    if not os.path.exists("blockchain"):
        os.makedirs("blockchain")

    if not os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, "w") as f:
            json.dump([], f)

    with open(BLOCKCHAIN_FILE, "r") as f:
        chain = json.load(f)

    previous_hash = chain[-1]["block_hash"] if chain else "0"

    block = {
        "evidence_id": evidence_id,
        "evidence_hash": hash_value,
        "timestamp": str(datetime.now()),
        "previous_hash": previous_hash
    }

    block_hash = calculate_block_hash(block)
    block["block_hash"] = block_hash

    chain.append(block)

    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

    print("Block added to blockchain")