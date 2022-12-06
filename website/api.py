import requests
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from .models import Note, ImageSet, Image
from .models import ImageSet, Image, RenderedModel
import sqlite3
from . import db
import json
import os
import socket
import threading
import socketio


api = Blueprint('api', __name__)
userToken = '1234567890'

def dbConnect():
    global conn
    conn = sqlite3.connect('/var/www/instance/database.db')
    global curs
    curs = conn.cursor()


### API Receive ###

## Api which saves image names and imageset id to a sqlite database, but also saves user_id to the imageset table
@api.route('/saveImages', methods=['POST'])
def saveImages():
    data = request.get_json()
    print(data)
    imageNames = data['imageName']
    imageSetId = data['imageSetId']
    userId = data['userId']
    token = data['token']

    if token == userToken:
        try:
            dbConnect()
            curs.execute("INSERT INTO image_set (user_id) VALUES (?)", (str(userId)))
            conn.commit()
            for imageName in imageNames:
                curs.execute("INSERT INTO image (image_name, imageset_id) VALUES (?, ?)", (imageName, imageSetId))
                conn.commit()
            conn.close()
            print("Success")
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})
            
## Api which saves rendered model_name , user_id and imageset_id to a sqlite database, inside a try catch block which returns exeption as e if fails, the call needs to be verified with a token
@api.route('/saveModel', methods=['POST'])
def saveModel():
    data = request.get_json()
    print(data)
    modelName = data['modelName']
    userId = data['userId']
    imageSetId = data['imageSetId']
    token = data['token']
    print(modelName)
    print(userId)
    print(imageSetId)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            curs.execute("INSERT INTO Rendered_Model (model_name, user_id, imageset_id) VALUES (?, ?, ?)", (modelName, userId, imageSetId))
            conn.commit()
            conn.close()
            print("Success")
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## saves a job to render so the client PC can ask for open jobs, and then innerjoin the rest to get a list of images to download with SFTP
@api.route('/saveJob', methods=['POST'])
def saveJob():
    data = request.get_json()
    print(data)
    status = data['status']
    userId = data['userId']
    imageSetId = data['imageSetId']
    token = data['token']
    print(status)
    print(userId)
    print(imageSetId)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            curs.execute("INSERT INTO Job (status, user_id, imageset_id) VALUES (?, ?, ?)", (status, userId, imageSetId))
            conn.commit()
            conn.close()
            print("Success")
            return jsonify({'message': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Api which gets all job which are set to render in status, and innerjoin the imageSet with the Image table on imageset_id
@api.route('/getJob', methods=['POST'])
def getJob():
    data = request.get_json()
    print(data)
    status = data['status']
    token = data['token']
    imageSetId = data['imageSetId']
    status = data['status']
    print(status)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            #curs.execute("SELECT Image.image_name FROM Image WHERE Image.imageset_id = ? AND Job.status = ?", (imageSetId, status))
            curs.execute("SELECT * FROM Job INNER JOIN Image ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            #curs.execute("SELECT Image.image_name FROM Image INNER JOIN Job ON ? = Image.imageset_id AND Job.status = ?", (imageSetId, status))
            rows = curs.fetchall()
            
            #print(json.dumps( [dict(ix) for ix in rows] ))
            conn.close()
            print("jsondump")
            print(json.dumps(rows))
            return json.dumps(rows)
        except Exception as e:
            print(e)
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})



## Api which deletes a rendered model from the sqlite database 
# where the rendered model Id equals the id supplied, the call needs to be verified with a token
@api.route('/deleteRenderedModel', methods=['DELETE'])
def deleteRenderedModel():
    data = request.get_json()
    print(data)
    id = data['id']
    token = data['token']
    print(id)
    print(token)
    if token == userToken:
        try:
            dbConnect()
            curs.execute("DELETE FROM RenderedModel WHERE id = ?", (id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})

## Api which deletes imageSet matching id, and delete all images with the same imageset_id from the sqlite database, the call needs to be verified with a token
@api.route('/deleteImageSetAndImages', methods=['DELETE'])
def deleteImageSetAndImages():
    data = request.get_json()
    print(data)
    id = data['id']
    token = data['token']
    print(id)
    print(token)
    if token == '123456789':
        try:
            dbConnect()
            curs.execute("DELETE FROM ImageSet WHERE id = ?", (id))
            conn.commit()
            curs.execute("DELETE FROM Image WHERE imageset_id = ?", (id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'success'})
        except Exception as e:
            return jsonify({'message': e})
    else:
        return jsonify({'message': 'token not valid'})





## Socket server which can send data to client through a new thread
# global socServer
# def socketServer():
#     # get the hostname
#     host = socket.gethostname()
#     port = 5001  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(2)
#     conn, address = server_socket.accept()  # accept new connection
#     print("Connection from: " + str(address))
#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print("from connected user: " + str(data))
#         data = input(' -> ')
#         conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection
#     socServer.join() # close the thread



# socServer = threading.Thread(target=socketServer, args=(), daemon=True)
# socServer.start()











### API Send Example ###
## Json example for imageSets with userId and multiple imagesNames
exampleImageJson = {
    "userId": 1,
    "token": "1234567890",
    "imageSetId": 1,
    "imageName": [ "01_a.jpg", "01_b.png", "01_c.png"]
    }

exampleModelJson = {
    "token": "1234567890",
    "modelName": "modelOne",
    "imageSetId": 1,
    "userId": 1
    }

exampleJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 1
}

exampleGetJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 1
}

## Exampple Python api call POST to saveJob api with the exampleJobJson to send
@api.route('/apisavejobexample', methods=['GET', 'POST'])
def apiSaveJobExample():
    try:
        url = "http://127.0.0.1:5000/saveJob"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

## Exampple Python api gets all open jobs connected to userID and imageSetId 
@api.route('/apigetjobexample', methods=['GET', 'POST'])
def apigetjobexample():
    try:
        url = "http://127.0.0.1:5000/getJob"
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers)
        response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers).json()
        print("The response:")
        print(response)
        # print(response.json())
        # responseJson = response.json()
        print(response[1][5]) # Prints out the imageName in the json array index position 5
        imageNames = []
        # For each in the response, append to a list all the values of the response[*][i] image names, and checks for duplicate names
        for i in range(len(response)):
            print(response[i][5])
            if response[i][5] not in imageNames:
                imageNames.append(response[i][5])
        print(imageNames)
        return json.dumps(response)
    except Exception as e:
        print(e)
        return "Error"


        

## Example Python api call which POST to a remote server api with a json object which uses the exampleJson format in a try catch block
@api.route('/apiimagesendexample', methods=['GET', 'POST'])
def apiImageSendExample():
    try:
        url = "http://127.0.0.1:5000/saveImages"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleImageJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

@api.route('/apimodelsendexample', methods=['GET', 'POST'])
def apiModelSendExample():
    try:
        url = "http://127.0.0.1:5000/saveModel"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleModelJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"
#######################