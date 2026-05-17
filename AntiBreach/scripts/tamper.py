
import json
import random
import os
import copy

def tamper_log_in_batch(batch_data):
    """
    Simulates tampering by modifying a random log entry in a batch.

    Args:
        batch_data (dict): The original batch data.

    Returns:
        dict: The tampered batch data.
    """
    # Deep copy to avoid modifying the original data
    tampered_data = copy.deepcopy(batch_data)
    
    # Check if there are any logs to tamper with
    if not tampered_data.get("logs"):
        print("No logs in the batch to tamper with.")
        return tampered_data

    # Select a random log to tamper
    log_index = random.randint(0, len(tampered_data["logs"]) - 1)
    log_to_tamper = tampered_data["logs"][log_index]
    
    print(f"Tampering with log at index {log_index}: {log_to_tamper}")

    # Modify a field, for example, the status or IP address
    # This is a simple example; more sophisticated tampering could be implemented
    if "status" in log_to_tamper:
        original_status = log_to_tamper["status"]
        log_to_tamper["status"] = "tampered"
        print(f"Changed status from '{original_status}' to 'tampered'")
    elif "ip_address" in log_to_tamper:
        original_ip = log_to_tamper["ip_address"]
        log_to_tamper["ip_address"] = "0.0.0.0"
        print(f"Changed IP address from {original_ip} to 0.0.0.0")
    else:
        # As a fallback, add a new field
        log_to_tamper["tampered"] = True
        print("Added 'tampered: True' to the log.")

    return tampered_data

if __name__ == '__main__':
    # Example batch data
    original_batch = {
      "batch_id": "batch_001",
      "logs": [
          {"log_id": 1, "status": "success", "ip_address": "192.168.1.1"},
          {"log_id": 2, "status": "failed", "ip_address": "10.0.0.5"}
      ],
      "hashes": ["hash1", "hash2"],
      "signatures": ["sig1", "sig2"],
      "merkle_root": "original_merkle_root"
    }

    print("Original Batch:")
    print(json.dumps(original_batch, indent=4))
    print("-" * 30)

    # Tamper the batch
    tampered_batch = tamper_log_in_batch(original_batch)

    print("\nTampered Batch:")
    print(json.dumps(tampered_batch, indent=4))
    print("-" * 30)
    
    print("Original batch remains unchanged:")
    print(json.dumps(original_batch, indent=4))

