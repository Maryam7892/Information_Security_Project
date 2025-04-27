from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt

# Generate public/private key pair
def generate_keys():
    public_key, private_key = generate_keypair()
    return public_key, private_key

# Encrypt a message using the public key
def encrypt_message(message: str, public_key: bytes):
    # `encrypt` returns a tuple: (ciphertext, shared_secret)
    ciphertext, _ = encrypt(public_key)
    return ciphertext

# Decrypt a ciphertext using the private key
def decrypt_message(ciphertext: bytes, private_key: bytes):
    try:
        shared_secret = decrypt(ciphertext, private_key)
        return shared_secret
    except Exception as e:
        return str(e)
