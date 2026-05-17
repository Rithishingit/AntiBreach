
import uuid

class LogBatcher:
    """
    A simple batching system for logs.
    """
    def __init__(self, batch_size=10):
        """
        Initializes the batcher with a specific batch size.

        Args:
            batch_size (int): The number of logs to include in each batch.
        """
        self.batch_size = batch_size
        self.current_batch = []
        self.batch_id_counter = 0

    def add_log(self, log_entry):
        """
        Adds a log to the current batch. If the batch becomes full, it returns the batch.

        Args:
            log_entry (dict): The log entry to add.

        Returns:
            dict or None: A dictionary representing the full batch, or None if the batch is not yet full.
        """
        self.current_batch.append(log_entry)
        if len(self.current_batch) >= self.batch_size:
            return self._create_batch()
        return None

    def _create_batch(self):
        """
        Creates a batch dictionary, assigns a batch ID, and resets the current batch.
        """
        self.batch_id_counter += 1
        batch_to_return = {
            "batch_id": f"batch_{self.batch_id_counter}",
            "logs": self.current_batch
        }
        self.current_batch = []
        return batch_to_return

    def get_remaining(self):
        """
        Returns any remaining logs that haven't been batched yet.
        """
        if self.current_batch:
            return self._create_batch()
        return None

if __name__ == '__main__':
    # Example Usage
    batcher = LogBatcher(batch_size=3)
    
    # Simulate receiving logs
    logs_to_process = [
        {"log_id": 1, "data": "event A"},
        {"log_id": 2, "data": "event B"},
        {"log_id": 3, "data": "event C"},
        {"log_id": 4, "data": "event D"},
        {"log_id": 5, "data": "event E"},
        {"log_id": 6, "data": "event F"},
        {"log_id": 7, "data": "event G"}
    ]

    for log in logs_to_process:
        print(f"Adding log: {log['log_id']}")
        batch = batcher.add_log(log)
        if batch:
            print(f"--- Batch created: {batch['batch_id']} with {len(batch['logs'])} logs ---")
            # print(batch)
            print("-" * 40)

    # Get any remaining logs that didn't form a full batch
    remaining_batch = batcher.get_remaining()
    if remaining_batch:
        print(f"--- Remaining batch created: {remaining_batch['batch_id']} with {len(remaining_batch['logs'])} logs ---")
        # print(remaining_batch)
        print("-" * 40)

    print("Log processing complete.")
