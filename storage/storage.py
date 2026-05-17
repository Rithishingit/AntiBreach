
import json
import os
from datetime import datetime

def save_to_cloud(batch_data, directory="data/cloud_storage"):
    """
    Saves the main log data (logs, hashes, signatures) to a 'cloud' file.
    The Merkle root is explicitly excluded.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    batch_id = batch_data.get("batch_id")
    if not batch_id:
        raise ValueError("Batch data must contain a 'batch_id'")

    cloud_data = {
        "batch_id": batch_id,
        "logs": batch_data.get("logs", []),
        "hashes": batch_data.get("hashes", []),
        "signatures": batch_data.get("signatures", []),
        "timestamp": datetime.now().isoformat()
    }

    file_path = os.path.join(directory, f"{batch_id}.json")
    with open(file_path, 'w') as f:
        json.dump(cloud_data, f, indent=4)

def save_to_blockchain(batch_id, merkle_root, file_path="data/blockchain_storage/blockchain.json"):
    """
    Appends the immutable record (batch_id, merkle_root, timestamp) to the 'blockchain' file.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    new_block = {
        "batch_id": batch_id,
        "merkle_root": merkle_root,
        "timestamp": datetime.now().isoformat()
    }

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                blockchain = json.load(f)
            except json.JSONDecodeError:
                blockchain = []
    else:
        blockchain = []

    blockchain.append(new_block)

    with open(file_path, 'w') as f:
        json.dump(blockchain, f, indent=4)

