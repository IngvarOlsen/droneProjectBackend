 ##### GENERATE private and public keys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

from Crypto.PublicKey import RSA

from hmac import compare_digest

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
# Get the public key associated with the private key
public_key = private_key.public_key()

# Get the private key in bytes format
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Get the public key in bytes format
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Open the private key file in write mode
with open('private_key.pem', 'wb') as private_key_file:
    # Write the private key data to the file
    private_key_file.write(private_key_bytes)

# Open the public key file in write mode
with open('public_key.pem', 'wb') as public_key_file:
    # Write the public key data to the file
    public_key_file.write(public_key_bytes)

######
# Check if keys match
######

# Read the secret key from the file
with open('private_key.pem', 'r') as secret_key_file:
    secret_key = RSA.importKey(secret_key_file.read())

# Read the public key from the file
with open('public_key.pem', 'r') as public_key_file:
    public_key = RSA.importKey(public_key_file.read())

# Check if the keys match
if secret_key.publickey() == public_key:
    print('The keys match')
else:
    print('The keys do not match')



# # Load the private key from the file
# with open('private_key.pem', 'rb') as private_key_file:
#     private_key = load_pem_private_key(private_key_file, password=None, backend=default_backend())

# # Load the public key from the file
# with open('public_key.pem', 'rb') as public_key_file:
#     public_key = load_pem_public_key(public_key_file, backend=default_backend())

# # Get the public key associated with the private key
# public_key = private_key.public_key()

# # Get the public key in bytes format
# public_key_bytes = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Compare the public key in bytes format with the original public key
# if compare_digest(public_key_bytes, public_key_bytes):
#     print("The saved keys match")
#     # The saved keys match
#     # Do something here
# # else:
# #     # The saved keys do not match
# #     # Do something else here





#####################
### CHECK for key match
#####################
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.serialization import load_pem_private_key
# from cryptography.hazmat.primitives.serialization import load_pem_public_key
# from cryptography.exceptions import InvalidSignature
# from hmac import compare_digest

# # Load the private key from the POST request
# private_key = load_pem_private_key(request.form['private_key'], password=None, backend=default_backend())

# # Get the public key associated with the private key
# public_key = private_key.public_key()

# # Get the public key in bytes format
# public_key_bytes = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Compare the public key in bytes format with the original public key
# if compare_digest(public_key_bytes, original_public_key):
#     # The private key matches the public key
#     # Do something here
#     else:
#     # The private key does not match the public key
#     # Do something else here






# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding

# # Generate a private-public key pair for the user
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048
# )
# public_key = private_key.public_key()

# # Serialize the keys for storage or transmission
# private_key_bytes = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )
# public_key_bytes = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Save the keys to a file or database for later use
# with open('private_key.pem', 'wb') as f:
#     f.write(private_key_bytes)

# with open('public_key.pem', 'wb') as f:
#     f.write(public_key_bytes)

# # In your Flask API code, you can use the private key to sign the data
# # being sent to the API and the public key to verify the signature
# @app.route('/api/savedImagesToSQlite', methods=['POST'])
# def savedImagesToSQlite():
#     # Load the private key from the file or database
#     with open('private_key.pem', 'rb') as f:
#         private_key_bytes = f.read()

#     private_key = serialization.load_pem_private_key(
#         private_key_bytes,
#         password=None,
#         backend=default_backend()
#     )

#     # Sign the data using the private key
#     data = request.get_json()
#     signature = private_key.sign(
#         data,
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA256()),
#             salt_length=padding.PSS.MAX_LENGTH
#         ),
#         hashes.SHA256()
#     )

#     # Include the signature in the response
#     return jsonify({
#         'data': data,
#         'signature': signature
#     })

# # On the client side, you can use the public key to verify the signature
# @app.route('/client', methods=['POST'])
# def client():
#     # Load the public key from the file or database
#     with open('public_key.pem', 'rb') as f:
#         public_key_bytes = f.read()

#     public_key = serialization.load_pem_public_key(
#         public_key_bytes,
#         backend=default_backend()
#     )

#     # Verify the signature using the public key
#     data = request.get_json()
#     signature = data['signature']
#     public_key.verify(
#         signature,
#         data['data'],
#         padding.PSS(),
#         hashes.SHA256()
#     )
