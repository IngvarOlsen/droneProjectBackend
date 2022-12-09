from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Generate a private-public key pair for the user
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Serialize the keys for storage or transmission
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the keys to a file or database for later use
with open('private_key.pem', 'wb') as f:
    f.write(private_key_bytes)

with open('public_key.pem', 'wb') as f:
    f.write(public_key_bytes)

# In your Flask API code, you can use the private key to sign the data
# being sent to the API and the public key to verify the signature
@app.route('/api/savedImagesToSQlite', methods=['POST'])
def savedImagesToSQlite():
    # Load the private key from the file or database
    with open('private_key.pem', 'rb') as f:
        private_key_bytes = f.read()

    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )

    # Sign the data using the private key
    data = request.get_json()
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Include the signature in the response
    return jsonify({
        'data': data,
        'signature': signature
    })

# On the client side, you can use the public key to verify the signature
@app.route('/client', methods=['POST'])
def client():
    # Load the public key from the file or database
    with open('public_key.pem', 'rb') as f:
        public_key_bytes = f.read()

    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )

    # Verify the signature using the public key
    data = request.get_json()
    signature = data['signature']
    public_key.verify(
        signature,
