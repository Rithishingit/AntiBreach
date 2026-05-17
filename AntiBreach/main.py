
import os
import json
import time
import random
import threading
from colorama import init, Fore, Style
from log_generator.log_generator import generate_log_entry
from ingestion.hasher.hasher import hash_log
from ingestion.signer.signer import sign_hash, get_public_key
from ingestion.batcher.batcher import LogBatcher
from ingestion.merkle.merkle import build_merkle_tree
from storage.storage import save_to_cloud, save_to_blockchain
from verification.verification import Verifier

# Initialize colorama
init(autoreset=True)

# Define storage locations
CLOUD_STORAGE_DIR = "data/cloud_storage"
BLOCKCHAIN_STORAGE_FILE = "data/blockchain_storage/blockchain.json"

def log_generation_thread(batcher):
    """
    A thread that continuously generates logs and creates new batches.
    """
    print(Fore.CYAN + "Log generation thread started.")
    while True:
        try:
            log = generate_log_entry()
            batch = batcher.add_log(log)

            if batch:
                print(Fore.BLUE + f"New batch created: {batch['batch_id']}. Processing...")
                
                hashes = [hash_log(l) for l in batch['logs']]
                signatures = [sign_hash(h).hex() for h in hashes]
                merkle_root = build_merkle_tree(hashes)
                
                batch_data_for_cloud = {
                    "batch_id": batch['batch_id'],
                    "logs": batch['logs'],
                    "hashes": hashes,
                    "signatures": signatures,
                }
                
                # 1. Save main data to cloud storage
                save_to_cloud(batch_data_for_cloud, directory=CLOUD_STORAGE_DIR)
                
                # 2. Save immutable record to blockchain storage
                save_to_blockchain(batch['batch_id'], merkle_root, file_path=BLOCKCHAIN_STORAGE_FILE)
                
                print(Fore.GREEN + f"Batch {batch['batch_id']} successfully processed and stored.")

            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(Fore.RED + f"Error in log generation thread: {e}")
            time.sleep(5)


def monitor_directory(verifier):
    """
    Continuously monitors the cloud storage directory for file changes and triggers verification.
    """
    file_states = {}
    loop_count = 0
    
    print(Fore.CYAN + "File monitoring thread started.")
    
    try:
        while True:
            time.sleep(4)
            change_detected = False
            
            if not os.path.exists(CLOUD_STORAGE_DIR):
                continue

            for filename in os.listdir(CLOUD_STORAGE_DIR):
                if not filename.endswith(".json"):
                    continue
                
                file_path = os.path.join(CLOUD_STORAGE_DIR, filename)
                current_mod_time = os.path.getmtime(file_path)
                last_mod_time = file_states.get(filename)

                if last_mod_time is None:
                    file_states[filename] = current_mod_time
                    change_detected = True

                elif current_mod_time > last_mod_time:
                    change_detected = True
                    batch_id = filename.replace(".json", "")
                    status, reasons = verifier.verify_batch(batch_id)
                    
                    if status == "TAMPERED":
                        print("\n" + Fore.RED + "="*60)
                        print(Fore.RED + Style.BRIGHT + "ALERT: INTEGRITY VIOLATION DETECTED")
                        print(Fore.RED + f"  - Batch ID: {batch_id}")
                        for reason in reasons:
                            print(Fore.YELLOW + f"    - Reason: {reason}")
                        print(Fore.RED + "="*60)
                    
                    file_states[filename] = current_mod_time
            
            if not change_detected:
                loop_count += 1
                if loop_count % 5 == 0:
                    print(Fore.GREEN + "STATUS: VERIFIED")

    except KeyboardInterrupt:
        pass


def main():
    """
    Main function to run the live monitoring simulation.
    """
    print(Fore.CYAN + "SOC Monitor Active")
    print(Fore.CYAN + "Initializing system...")
    
    # Clean up previous data
    for dir_path in [CLOUD_STORAGE_DIR, os.path.dirname(BLOCKCHAIN_STORAGE_FILE)]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for f in os.listdir(dir_path):
            if f.endswith(".json"):
                os.remove(os.path.join(dir_path, f))

    # Initialization
    verifier = Verifier(get_public_key(), CLOUD_STORAGE_DIR, BLOCKCHAIN_STORAGE_FILE)
    batcher = LogBatcher(batch_size=10)

    # Start threads
    gen_thread = threading.Thread(target=log_generation_thread, args=(batcher,), daemon=True)
    gen_thread.start()

    try:
        monitor_directory(verifier)
    except KeyboardInterrupt:
        print("\n" + Fore.CYAN + "--- SOC Monitor shutting down. ---")


if __name__ == "__main__":
    main()
