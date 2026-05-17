
import json
import os
import sys

# Add the project root to the python path to allow importing modules correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.hasher.hasher import hash_log
from ingestion.merkle.merkle import build_merkle_tree
from ingestion.signer.signer import verify_signature

class Verifier:
    """
    Verifies the integrity of log batches by comparing cloud data against a blockchain record.
    """
    def __init__(self, public_key, cloud_dir, blockchain_file):
        """
        Initializes the verifier.
        """
        self.public_key = public_key
        self.cloud_dir = cloud_dir
        self.blockchain_file = blockchain_file

    def verify_batch(self, batch_id):
        """
        Verifies a single batch file from the cloud against the blockchain.
        """
        # 1. Load batch from cloud storage
        cloud_file_path = os.path.join(self.cloud_dir, f"{batch_id}.json")
        if not os.path.exists(cloud_file_path):
            return "TAMPERED", [f"Cloud data for batch '{batch_id}' not found."]

        with open(cloud_file_path, 'r') as f:
            try:
                cloud_data = json.load(f)
            except json.JSONDecodeError:
                return "TAMPERED", [f"Failed to decode JSON from cloud file for batch '{batch_id}'."]

        # 2. Recompute hashes and Merkle root from cloud data
        logs = cloud_data.get("logs", [])
        recomputed_hashes = [hash_log(log) for log in logs]
        recomputed_merkle_root = build_merkle_tree(recomputed_hashes)

        # 3. Fetch corresponding root from blockchain storage
        if not os.path.exists(self.blockchain_file):
            return "TAMPERED", ["Blockchain storage file not found."]

        with open(self.blockchain_file, 'r') as f:
            try:
                blockchain_data = json.load(f)
                blockchain_record = next((item for item in blockchain_data if item["batch_id"] == batch_id), None)
            except (json.JSONDecodeError, StopIteration):
                blockchain_record = None
        
        if not blockchain_record:
            return "TAMPERED", [f"No record for batch '{batch_id}' found in the blockchain."]

        stored_merkle_root = blockchain_record.get("merkle_root")

        # 4. Compare both roots
        if recomputed_merkle_root != stored_merkle_root:
            return "TAMPERED", [f"Merkle root mismatch for batch '{batch_id}'. The data in the cloud has been altered."]

        # Optional: Deeper check for internal consistency (hashes and signatures)
        original_hashes = cloud_data.get("hashes", [])
        signatures_hex = cloud_data.get("signatures", [])
        for i in range(len(logs)):
            if recomputed_hashes[i] != original_hashes[i] or not verify_signature(recomputed_hashes[i], bytes.fromhex(signatures_hex[i]), self.public_key):
                 return "TAMPERED", [f"Internal data inconsistency (hash or signature) at log index {i} in batch '{batch_id}'."]

        return "VERIFIED", ["All checks passed."]


