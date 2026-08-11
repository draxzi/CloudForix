import json

BLOCKCHAIN_FILE = "blockchain/blockchain.json"

def verify_integrity(evidence_id, new_hash):
    try:
        with open(BLOCKCHAIN_FILE, "r") as f:
            chain = json.load(f)

        for block in chain:
            if block["evidence_id"] == evidence_id:
                if block["evidence_hash"] == new_hash:
                    print("Integrity Verified")
                    return "Verified"
                else:
                    print("Integrity Compromised")
                    return "Compromised"

        return "No Record Found"

    except:
        return "Blockchain file not found"