# AntiBreach: Comprehensive User Guide

Welcome to the detailed user guide for **AntiBreach**. This document explains how the system works end-to-end, how to run it, and how to simulate a cyberattack to test the cryptographic defenses.

---

## 1. How the System Works

AntiBreach is built to emulate a zero-trust Security Operations Center (SOC) pipeline. Here is the lifecycle of a single log:

1. **Generation:** `log_generator.py` simulates incoming logs from Web Servers, Firewalls, and Intrusion Detection Systems (IDS).
2. **Ingestion & Batching:** Logs are grouped into batches (default size: 10 logs) by `batcher.py` to optimize processing.
3. **Hashing & Signing:** Each log in the batch is hashed using SHA-256 (`hasher.py`) and cryptographically signed (`signer.py`) using simulated RSA keys.
4. **Merkle Tree Construction:** The hashes are combined into a Merkle Tree (`merkle.py`). The final "Root Hash" perfectly represents the entire batch.
5. **Storage:** 
   - The raw logs and signatures are saved to local cloud storage (`data/cloud_storage`).
   - The Merkle Root is anchored to an immutable ledger (`data/blockchain_storage/blockchain.json`).

---

## 2. Running the Active SOC Monitor

To start the main system, open your terminal and run:

```bash
python main.py
```

### What happens when you run this?
- The system will automatically create the `data/cloud_storage` and `data/blockchain_storage` folders if they don't exist.
- A background thread starts generating dummy logs in real-time.
- You will see console output showing batches being created and securely anchored to the blockchain.
- A monitoring thread constantly watches the storage. If it detects changes, it runs a background verification.

*Press `Ctrl + C` in the terminal to stop the monitor.*

---

## 3. Simulating a Cyber Attack (Log Tampering)

A core feature of AntiBreach is detecting unauthorized log modifications. To test this, we will act as a malicious hacker trying to hide their tracks.

1. Ensure you have run `python main.py` at least once so that some batches exist in `data/cloud_storage/`.
2. Run the tamper script:

```bash
python scripts/tamper.py
```

### What happens when you run this?
- The script opens one of your verified batch files.
- It randomly alters a log (for example, changing a login status from `"failed"` to `'success'`, or altering an IP address).
- It saves the file back. To the naked eye, the log file looks normal.

---

## 4. Cryptographic Verification

Because the attacker altered the underlying data, the mathematical hash of that specific log changes. This causes a cascade: the Merkle Tree root changes, and it will no longer match the immutable root stored on the blockchain.

Run the manual verification script or watch the `main.py` live monitor:

```bash
python verification/verification.py
```

### What happens when you run this?
- The verifier loads the batch from cloud storage.
- It recalculates the SHA-256 hashes and reconstructs the Merkle Tree.
- It fetches the original Merkle Root from the blockchain ledger.
- **Result:** It will flash a Red Alert (`INTEGRITY VIOLATION DETECTED`), specifying exactly which batch was compromised.

---

## 5. Modifying Configuration

If you want to customize the behavior of AntiBreach, you can modify the following:
- **Batch Size:** Open `main.py` and change `LogBatcher(batch_size=10)` to a different number.
- **Log generation speed:** Open `main.py` and modify `time.sleep(random.uniform(1, 3))` in the `log_generation_thread` function to generate logs faster or slower.