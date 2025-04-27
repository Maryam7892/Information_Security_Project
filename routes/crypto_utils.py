
from kyber_py.kyber import Kyber512

# Generate public/private key pair
def generate_keys():
    public_key, private_key = Kyber512.keygen()  # Generate the key pair
    return public_key, private_key

# Encrypt a message using the public key
def encrypt_message(message: str, public_key: bytes):
    # Encrypt the message using Kyber512
    ciphertext, shared_secret = Kyber512.encaps(public_key)
    
    # Convert the message into bytes and return ciphertext
    message_bytes = message.encode('utf-8')
    return ciphertext

# Decrypt a ciphertext using the private key
def decrypt_message(ciphertext: bytes, private_key: bytes):
    try:
        # Decrypt the ciphertext and return the shared secret
        shared_secret = Kyber512.decaps(private_key, ciphertext)
        return shared_secret
    except Exception as e:
        return str(e)

# Example usage:
public_key, private_key = generate_keys()
message = "Hello, Kyber!"
ciphertext = encrypt_message(message, public_key)

print("Ciphertext:", ciphertext)

shared_secret = decrypt_message(ciphertext, private_key)
print("Shared secret after decryption:", shared_secret)
