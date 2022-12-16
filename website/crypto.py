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

## Normal key_size is 2048 but for the demo we only use 512
def privPublicKeys(exp=65537, key_size=512):
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=exp,
        key_size=key_size
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
    print('private_key_bytes: ' , private_key_bytes)
    print('public_key_bytes: ' , public_key_bytes)
    # print(checkKeysFromBytes(private_key_bytes, public_key_bytes))
    # print(write_keys_to_file(private_key_bytes, public_key_bytes))
    return private_key_bytes, public_key_bytes


######
# Check if keys match
######
def checkKeysFromBytes(private_key_bytes, public_key_bytes):
    # Read the secret key 
    secret_key = RSA.importKey(private_key_bytes)

    # Read the public key 
    public_key = RSA.importKey(public_key_bytes)

    # Check if the keys match
    if secret_key.publickey() == public_key:
        print('The keys match')
        return True
    else:
        print('The keys do not match')
        return False

## Reads public and private key from file and returns key in bytes format in tupple
def readKeysFromFile():
    # Read the secret key from the file
    with open('private_keyTest.pem', 'r') as secret_key_file:
        secret_key = RSA.importKey(secret_key_file.read())
        secret_key_bytes = secret_key.exportKey()

    # Read the public key from the file
    with open('public_keyTest.pem', 'r') as public_key_file:
        public_key = RSA.importKey(public_key_file.read())
        public_key_bytes = public_key.exportKey()
    return secret_key_bytes, public_key_bytes



## Writes keys to files
def write_keys_to_file(private_key_bytes, public_key_bytes):
    try:
        # Open the private key file in write mode
        with open('private_keyTest.pem', 'wb') as private_key_file:
            # Write the private key data to the file
            private_key_file.write(private_key_bytes)

        # Open the public key file in write mode
        with open('public_keyTest.pem', 'wb') as public_key_file:
            # Write the public key data to the file
            public_key_file.write(public_key_bytes)
    except Exception as e:
        print(e)
        return "Error writing keys to file"


## Test calls

# privPublicKeys()
# write_keys_to_file(privPublicKeys()[0], privPublicKeys()[1])
# 
checkKeysFromBytes(readKeysFromFile()[0], readKeysFromFile()[1])