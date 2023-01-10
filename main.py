from website import create_app, create_database
from sanic import Sanic
from sanic.response import html
from flask import send_from_directory
import base64
import hashlib
import random
import socketio
import os


randomHash=hashlib.md5(os.urandom(4)).digest(); randomHash=base64.b64encode(randomHash); 
print(randomHash)


app = create_app()
app.config['UPLOAD_FOLDER'] = 'sftp/images'


app.config['SECRET_KEY'] = "UbhodfUMwmeZTyjZ7r0B0g=="
# app.static_url_path = '/sftp/images'
#create_database(app)


@app.route('/images/<path:filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], 
        filename
    )

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=('cert.pem', 'certpriv_key.pem')) # For SSL
