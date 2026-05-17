
class BlockchainMock:
    """
    A simple mock of a blockchain for storing Merkle roots.
    """
    def __init__(self):
        """
        Initializes the blockchain mock with an empty storage.
        """
        self.chain = {}
        print("Blockchain Mock initialized.")

    def store_merkle_root(self, batch_id, merkle_root):
        """
        Stores a Merkle root on the 'blockchain'.

        Args:
            batch_id (str): The ID of the batch.
            merkle_root (str): The Merkle root to store.
        """
        if batch_id in self.chain:
            print(f"Warning: Batch ID {batch_id} already exists. Overwriting.")
        
        self.chain[batch_id] = merkle_root
        print(f"Stored Merkle root for batch {batch_id}: {merkle_root}")

    def get_merkle_root(self, batch_id):
        """
        Retrieves a Merkle root from the 'blockchain'.

        Args:
            batch_id (str): The ID of the batch to retrieve.

        Returns:
            str or None: The Merkle root if found, otherwise None.
        """
        return self.chain.get(batch_id)

if __name__ == '__main__':
    # Example Usage
    blockchain = BlockchainMock()

    # Store some Merkle roots
    blockchain.store_merkle_root("batch_001", "merkle_root_of_batch_1")
    blockchain.store_merkle_root("batch_002", "merkle_root_of_batch_2")
    
    print("-" * 20)

    # Retrieve a Merkle root
    retrieved_root = blockchain.get_merkle_root("batch_001")
    if retrieved_root:
        print(f"Retrieved Merkle root for batch_001: {retrieved_root}")
    else:
        print("Merkle root for batch_001 not found.")

    # Try to retrieve a non-existent root
    non_existent_root = blockchain.get_merkle_root("batch_999")
    if non_existent_root:
        print(f"Retrieved Merkle root for batch_999: {non_existent_root}")
    else:
        print("Merkle root for batch_999 not found, as expected.")

    print("-" * 20)
    print("Current state of the blockchain mock:")
    print(blockchain.chain)
