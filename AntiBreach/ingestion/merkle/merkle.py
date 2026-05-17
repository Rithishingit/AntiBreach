
import hashlib

def hash_pair(hash1, hash2):
    """Hashes two concatenated hashes."""
    # Ensure inputs are bytes
    if isinstance(hash1, str):
        hash1 = hash1.encode('utf-8')
    if isinstance(hash2, str):
        hash2 = hash2.encode('utf-8')
        
    # Concatenate and hash
    combined = hash1 + hash2
    return hashlib.sha256(combined).hexdigest()

def build_merkle_tree(list_of_hashes):
    """
    Builds a Merkle Tree from a list of hashes and returns the Merkle root.

    Args:
        list_of_hashes (list): A list of hex digest strings.

    Returns:
        str: The Merkle root hash.
    """
    # Handle edge cases
    if not list_of_hashes:
        return None
    if len(list_of_hashes) == 1:
        return list_of_hashes[0]

    # Start with the initial list of hashes
    current_level = list_of_hashes

    # Continue processing until we have a single root hash
    while len(current_level) > 1:
        next_level = []
        
        # If the number of hashes is odd, duplicate the last one
        if len(current_level) % 2 != 0:
            current_level.append(current_level[-1])
            
        # Process in pairs
        for i in range(0, len(current_level), 2):
            hash1 = current_level[i]
            hash2 = current_level[i+1]
            next_level.append(hash_pair(hash1, hash2))
            
        # Move to the next level
        current_level = next_level
        
    # The final hash is the Merkle root
    return current_level[0]

if __name__ == '__main__':
    # Example list of transaction hashes (as hex strings)
    tx_hashes = [
        hashlib.sha256(b"tx1").hexdigest(),
        hashlib.sha256(b"tx2").hexdigest(),
        hashlib.sha256(b"tx3").hexdigest(),
        hashlib.sha256(b"tx4").hexdigest(),
        hashlib.sha256(b"tx5").hexdigest() # Odd number of hashes
    ]

    print("Initial Hashes:")
    for h in tx_hashes:
        print(h)
    
    print("\nBuilding Merkle Tree...")
    
    # Build the Merkle Tree
    merkle_root = build_merkle_tree(tx_hashes)
    
    print(f"\nMerkle Root: {merkle_root}")

    # Example with an even number of hashes
    tx_hashes_even = tx_hashes[:4]
    print("\nBuilding Merkle Tree with even number of hashes...")
    merkle_root_even = build_merkle_tree(tx_hashes_even)
    print(f"\nMerkle Root (Even): {merkle_root_even}")
