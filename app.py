from flask import Flask, render_template, request
from flask_talisman import Talisman
from dotenv import load_dotenv
import os
from routes.crypto_utils import generate_keys, encrypt_message, decrypt_message

app = Flask(__name__)
Talisman(app)
app.secret_key = os.getenv("SECRET_KEY", "fallbacksecret")

# Declare global variables for public and private keys
public_key = None
private_key = None

@app.route('/')
def home():
    return render_template('index.html', public_key=public_key, private_key=private_key)

@app.route('/generate_keys', methods=['POST'])
def handle_keygen():
    global public_key, private_key
    public_key, private_key = generate_keys()
    # Render the page with the new public and private keys
    return render_template('index.html', public_key=public_key.hex(), private_key=private_key.hex())

# Encrypts the user-submitted message using the provided public key,
#  or it will fallback to the globally stored public key if none provided.

@app.route('/encrypt', methods=['POST'])
def handle_encrypt():
    message = request.form['message']
    
    # Use provided public_key if it exists, otherwise use global public_key
    public_key_input = bytes.fromhex(request.form['public_key']) if request.form.get('public_key') else public_key
    
    ciphertext = encrypt_message(message, public_key_input)
    return render_template('index.html', ciphertext=ciphertext.hex(), public_key=request.form['public_key'], private_key=private_key.hex())

# Decrypts the submitted ciphertext using the provided private key,
#     or it will fallback to the globally stored private key if none provided.

@app.route('/decrypt', methods=['POST'])
def handle_decrypt():
    ciphertext = bytes.fromhex(request.form['ciphertext'])
    
    # Use provided private_key if it exists, otherwise use global private_key
    private_key_input = bytes.fromhex(request.form['private_key']) if request.form.get('private_key') else private_key
    
    decrypted = decrypt_message(ciphertext, private_key_input)

    # If decrypted is a string, pass it directly, otherwise convert to hex
    if isinstance(decrypted, bytes):
        decrypted = decrypted.hex()  # Convert to hex if it's in bytes

    return render_template('index.html', decrypted=decrypted, private_key=request.form['private_key'] if request.form.get('private_key') else private_key.hex(), public_key=public_key.hex())



if __name__ == '__main__':
    app.run(debug=True)
