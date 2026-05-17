
import json
import hashlib

def hash_log(log_entry):
    """
    Computes the SHA-256 hash of a log entry.

    Args:
        log_entry (dict): The log entry to hash.

    Returns:
        str: The SHA-256 hash as a hex digest.
    """
    # Convert the dictionary to a canonical JSON string (sorted keys)
    canonical_log = json.dumps(log_entry, sort_keys=True, separators=(',', ':'))
    
    # Encode the string to bytes
    log_bytes = canonical_log.encode('utf-8')
    
    # Compute the SHA-256 hash
    sha256_hash = hashlib.sha256(log_bytes)
    
    # Return the hash as a hex digest
    return sha256_hash.hexdigest()

if __name__ == '__main__':
    # Example log entry
    example_log = {
        "timestamp": "2024-05-20T10:00:00",
        "source": "web_server",
        "ip_address": "192.168.1.1",
        "user_id": "user_1234",
        "event_type": "login_success",
        "status": "success"
    }

    # Another log with same data but different key order
    example_log_disordered = {
        "status": "success",
        "event_type": "login_success",
        "user_id": "user_1234",
        "ip_address": "192.168.1.1",
        "source": "web_server",
        "timestamp": "2024-05-20T10:00:00"
    }

    # Hash the log entries
    log_hash1 = hash_log(example_log)
    log_hash2 = hash_log(example_log_disordered)

    print(f"Log Entry 1: {example_log}")
    print(f"SHA-256 Hash 1: {log_hash1}")
    print("-" * 20)
    print(f"Log Entry 2 (disordered): {example_log_disordered}")
    print(f"SHA-256 Hash 2: {log_hash2}")
    print("-" * 20)

    # Verify that the hashes are identical, demonstrating canonical representation
    assert log_hash1 == log_hash2
    print("Hashes are identical, as expected.")
