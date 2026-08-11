import json
import os
from datetime import datetime

ACCESS_LOG = "blockchain/access_log.json"

def log_access(evidence_id, investigator):
    record = {
        "evidence_id": evidence_id,
        "investigator": investigator,
        "timestamp": str(datetime.now())
    }

    if os.path.exists(ACCESS_LOG):
        with open(ACCESS_LOG, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(ACCESS_LOG, "w") as f:
        json.dump(data, f, indent=4)

    return record