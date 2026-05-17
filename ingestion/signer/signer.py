
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# Generate a persistent key pair for the purpose of this simulation
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

def get_public_key():
    """Returns the public key."""
    return public_key

def sign_hash(data_hash):
    """
    Signs a hash using the private key.

    Args:
        data_hash (str): The hex digest of the hash to be signed.

    Returns:
        bytes: The signature.
    """
    # The hash needs to be in bytes
    hash_bytes = bytes.fromhex(data_hash)
    
    signature = private_key.sign(
        hash_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(data_hash, signature, pub_key):
    """
    Verifies a signature using the public key.

    Args:
        data_hash (str): The hex digest of the hash.
        signature (bytes): The signature to verify.
        pub_key: The public key to use for verification.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    hash_bytes = bytes.fromhex(data_hash)
    
    try:
        pub_key.verify(
            signature,
            hash_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

if __name__ == '__main__':
    # Example Usage
    test_hash = hashes.Hash(hashes.SHA256())
    test_hash.update(b"some data to sign")
    data_to_sign = test_hash.finalize().hex()

    print(f"Data Hash: {data_to_sign}")

    # Sign the data
    signature = sign_hash(data_to_sign)
    print(f"Signature (first 16 bytes): {signature[:16].hex()}...")

    # Verify the signature
    is_valid = verify_signature(data_to_sign, signature, get_public_key())
    
    print(f"\nSignature verification successful: {is_valid}")
    assert is_valid

    # Tamper the data and try to verify
    tampered_hash = hashes.Hash(hashes.SHA256())
    tampered_hash.update(b"tampered data")
    tampered_data_hash = tampered_hash.finalize().hex()

    is_valid_tampered = verify_signature(tampered_data_hash, signature, get_public_key())
    print(f"Tampered data verification successful: {is_valid_tampered}")
    assert not is_valid_tampered
