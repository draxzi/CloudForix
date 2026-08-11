import json
import os
from datetime import datetime

CHAIN_FILE = "blockchain/chain.json"

def record_chain(evidence_id, action, investigator):
    if os.path.exists(CHAIN_FILE):
        with open(CHAIN_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = []

    record = {
        "evidence": evidence_id,
        "action": action,
        "investigator": investigator,
        "time": str(datetime.now())
    }

    data.append(record)

    with open(CHAIN_FILE, 'w') as f:
        json.dump(data, f, indent=4)