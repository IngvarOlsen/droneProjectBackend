from flask import Flask, request
from cryptography.fernet import Fernet
from flask import jsonify
from flask import request
import requests
import json
from base64 import b64encode, b64decode

app = Flask(__name__)

# Generate a private key for encrypting and decrypting data
private_key = Fernet.generate_key()

# Save the private key to a file
with open('private_key.key', 'wb') as key_file:
    key_file.write(private_key)

# Load the private key from the file
with open('private_key.key', 'rb') as key_file:
    private_key = key_file.read()

# Create a Fernet object using the private key
fernet = Fernet(private_key)

# Generate a public key from the private key
#public_key = fernet.public_key()

@app.route('/fernetTest', methods=['POST'])
def fernetTest():
    # Get the encrypted data from the request
    try:
        encrypted_data = request.get_json()['encrypted_data']

        # Decrypt the data using the private key
        decrypted_data = fernet.decrypt(encrypted_data)

        print(decrypted_data)

        # Save the decrypted data to the SQLite database
        # (Implementation details will vary depending on your specific use case)

        return 'Success'

    except:
        print("Error")
        return 'Error'
    

#Test function which sends a POST request to the /fernetTest endpoint with the encrypted json
@app.route('/test', methods=['GET','POST'])
def test():

    try:
        # Encrypt the data using the public key
        encrypted_data = fernet.encrypt(b'Hello World!')
        dataToSend = b64encode(encrypted_data).decode('utf-8')

        # Send the encrypted data to the API
        response = requests.post(
        'http://127.0.0.1:5000//fernetTest', 
        json={'encrypted_data': json.dumps(dataToSend)}
        )
        return 'Success'
    except:
        print("Error")
        return 'Error'
  
if __name__ == '__main__':
    app.run()