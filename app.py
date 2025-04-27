from flask import Flask, render_template, request, redirect, url_for, flash
from flask_talisman import Talisman
from dotenv import load_dotenv
from routes.crypto_utils import generate_keys, encrypt_message, decrypt_message

app = Flask(__name__)
Talisman(app)
app.secret_key = os.getenv("SECRET_KEY", "fallbacksecret")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_keys', methods=['POST'])
def handle_keygen():
    public_key, private_key = generate_keys()
    return render_template('index.html',
                           public_key=public_key.hex(),
                           private_key=private_key.hex())

@app.route('/encrypt', methods=['POST'])
def handle_encrypt():
    message = request.form['message']
    public_key = bytes.fromhex(request.form['public_key'])
    ciphertext = encrypt_message(message, public_key)
    return render_template('index.html',
                           ciphertext=ciphertext.hex(),
                           public_key=request.form['public_key'])

@app.route('/decrypt', methods=['POST'])
def handle_decrypt():
    ciphertext = bytes.fromhex(request.form['ciphertext'])
    private_key = bytes.fromhex(request.form['private_key'])
    decrypted = decrypt_message(ciphertext, private_key)
    return render_template('index.html',
                           decrypted=decrypted.hex(),
                           private_key=request.form['private_key'])

if __name__ == '__main__':
    app.run(debug=True)
