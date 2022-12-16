import requests
import pysftp
import json
import os
import subprocess

#print(os.listdir())
with open("C:\\src\\projects\\droneProject\\secrets.json") as s:
    secrets = json.loads(s.read())
    print(secrets["ip"])

exampleGetJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 2
}
exampleJobJson = {
    "token" : "1234567890",
    "status" : "render",
    "userId" : 1,
    "imageSetId" : 2
}
exampleModelUploadJson = {
    "token" : "1234567890",
    "s" : "complete",
    "userId" : 1,
    "imageSetId" : 2,
    "jobId" : 1,
}

imageJson = {
        "userId": 1,
        "token": "1234567890",
        "imageSetId": 3,
        "imageName": []
    }

imageNames = []
#Places the first index from the sql to the Jobinfo for later use when we upload a reference to the job and the 3d model to the server again
jobInfo = []
# meshroomBatch = "meshroom_batch -i 'C:\src\meshroomBox\input' -o 'C:\src\meshroomBox\output' --cache 'C:\src\meshroomBox\cache' --paramOverrides FeatureExtraction:forceCpuExtraction=0"

# p = subprocess.Popen(["meshroom_batch"], cwd=r"C:\src\projects\droneProject\Meshroom-2021.1.0")
# p.wait()
# print(p.returncode())


# list_files = subprocess.run(["ls", "-l"])
# print("The exit code was: %d" % list_files.returncode)


def getMaxImageSetId():
    try:
        url = "http://"+ secrets["ip"] + ":5000/gethighestimagesetid"
        print(url)
        headers = {'Content-Type': "application/json"}
        response = requests.get(url, data=json.dumps(1), headers=headers)
        print("Max ID is ")
        maxId = response.json()
        print(maxId[0][0]) 
        return maxId[0][0]
    except Exception as e:
        print(e)
        return e
#getMaxImageSetId()

def sftpDownload():
    with pysftp.Connection('129.151.211.178', username='ftpuser', private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
        print("Connection established.")

        # Looping through imageNames and appends imageNames[i] to the remoteFilePath and localFilepath name
        for i in range(len(imageNames)):
            remoteFilePath = "sftp/" + imageNames[i]
            #localFilePath = fr"C:\src\projects\droneProject\meshroomBox\input\{imageNames[i]}"
            localFilePath = fr"C:\src\projects\droneProject\sftp\{imageNames[i]}"
            try:
                sftp.get(remoteFilePath,localFilePath)
            except Exception as e:
                print(e)
        sftp.close()        
        # sftp.put_d('/home/rpi666/Desktop/cam_images','/ftpuser/eriksmappe/')  # upload file to public/ on remote
        # print("Data sent!")
        print("Closing SFTP connection.")

#Uploads a images to the sftp server
# def sftpUpload():
#     with pysftp.Connection('129.151.211.178', username='ftpuser', private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
#         print("Connection established.")
#         try:
        
#         exec
#         for name in os.listdir(r"C:\src\projects\droneProject\upload"):
#             print(name)
    
   

def apigetjob():
    global imageNames 
    global jobInfo
    try:
        url = "http://129.151.211.178:5000/getJob"
        headers = {'Content-Type': 'application/json'}
        #response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers)
        response = requests.post(url, data=json.dumps(exampleJobJson), headers=headers).json()
        print("The response:")
        print(response)
        # print(response.json())
        # responseJson = response.json()
        print(response[1][5]) # Prints out the imageName in the json array index position 5
        # Saves the first index of the response to the jobInfo list for when we upload the 3d model and the job reference to the server
        jobInfo.append(response[0])
        # For each in the response, append to a list all the values of the response[*][i] image names, and checks for duplicate names
        for i in range(len(response)):
            print(response[i][5])
            if response[i][5] not in imageNames:
                imageNames.append(response[i][5])
        print(imageNames)
        #sftpDownload(imageNames)
        return json.dumps(response)
    except Exception as e:
        print(e)
        return "Error"




def sftpDownloadTest():
    with pysftp.Connection('129.151.211.178', username='ftpuser', private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
        print("Connection established.")

        



        # remoteFilePath = "/var/www/website/static/sftp/models/texture_1001.png"
        # localFilePath = fr"C:\src\projects\droneProject\sftp\test.png"
        print(sftp.listdir())
        try:
            #sftp.get(remoteFilePath,localFilePath)
            #Downloads with sftp.get for every image in the imageNames list
            for i in range(len(imageNames)):
                remoteFilePath = "/var/www/website/static/sftp/images/" + imageNames[i]
                localFilePath = fr"C:\src\projects\droneProject\meshroomBox\input\{imageNames[i]}"
                #localFilePath = fr"C:\src\projects\droneProject\sftp\{imageNames[i]}"
                print("Downloading file: " + imageNames[i])
                sftp.get(remoteFilePath,localFilePath)
            print("File downloaded")
        except Exception as e:
            print("Error")
            print(e)
        sftp.close()        
        # sftp.put_d('/home/rpi666/Desktop/cam_images','/ftpuser/eriksmappe/')  # upload file to public/ on remote
        # print("Data sent!")
        print("Closing SFTP connection.")


def sftpUploadTest():
    
    with pysftp.Connection('129.151.211.178', username='ftpuser' , private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
        print("Connection established.")

        remoteFilePath = "/var/www/website/static/sftp/images/test.png"
        localFilePath = fr"C:\src\projects\droneProject\sftp\test.png"
        print(sftp.listdir())
        try:
            sftp.put(localFilePath, remoteFilePath)
            print("File Uploaded")
        except Exception as e:
            print("Error")
            print(e)
        sftp.close()        
        # sftp.put_d('/home/rpi666/Desktop/cam_images','/ftpuser/eriksmappe/')  # upload file to public/ on remote
        # print("Data sent!")
        print("Closing SFTP connection.")


def MeshroomBatch():

    inputFrames = 'C:\\src\\projects\\droneProject\\meshroomBox\\input'
    outputMesh = 'C:\\src\\projects\\droneProject\\meshroomBox\\output'
    meshroomCache = 'C:\\src\\projects\\droneProject\\meshroomBox\\cache'

    process = subprocess.run(
            [
                "C:\\src\\projects\\droneProject\\Meshroom-2021.1.0\\meshroom_batch.exe",
                '--input',
                inputFrames,
                '--output',
                outputMesh,
                '--cache',
                meshroomCache,
                "--paramOverrides",
                "FeatureExtraction:forceCpuExtraction=0"
            ],
            check=True
        )
    print(process)
    print("Meshroom batch complete")

def MeshroomBatchTest():
    inputFrames = 'C:\\src\\projects\\droneProject\\meshroomBox\\input\\testGround'
    outputMesh = 'C:\\src\\projects\\droneProject\\meshroomBox\\output\\testGround'
    meshroomCache = 'C:\\src\\projects\\droneProject\\meshroomBox\\cache\\testGround'

    process = subprocess.run(
            [
                "C:\\src\\projects\\droneProject\\Meshroom-2021.1.0\\meshroom_batch.exe",
                '--input',
                inputFrames,
                '--output',
                outputMesh,
                '--cache',
                meshroomCache,
                "--paramOverrides",
                "FeatureExtraction:forceCpuExtraction=0"
            ],
            check=True
        )
    print(process)
    print("Meshroom batch complete")


## Uploads the rendered 3d model to the server
def sftpUploadModel():
     with pysftp.Connection('129.151.211.178', username='ftpuser' , private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
        print("Connection established.")

        remoteFilePath = "/var/www/website/static/sftp/models"
        localFilePath = fr"C:\src\projects\droneProject\meshroomBox\output\testGround"
        ## Check contents of the output folder
        dir = sftp.listdir()
        newRemote = "/var/www/website/static/sftp/models/" + "model_" + str(len(dir))
        print(newRemote)
        print(dir)
        ## Make a new directory in the folder to upload the model to
        sftp.execute("mkdir " + remoteFilePath + "/model_" + str(len(dir)))

        try:
            ## For every file in the output folder it uploads it to the server
            for file in os.listdir(localFilePath):
                print("Uploading file: " + file)
                sftp.put(localFilePath + "\\" + file, newRemote + "/" + file)
            #sftp.put(localFilePath, remoteFilePath)
            print("Files Uploaded")
        except Exception as e:
            print("Error")
            print(e)
        sftp.close()        
        # sftp.put_d('/home/rpi666/Desktop/cam_images','/ftpuser/eriksmappe/')  # upload file to public/ on remote
        # print("Data sent!")
        print("Closing SFTP connection.")


## Uploads the images to sftp server incase we need to do it from localhost
def sftpUploadImages():
     with pysftp.Connection('129.151.211.178', username='ftpuser' , private_key=r"C:\Users\Eirikur Gudbjørnsson\ssh_keys\sftp_ssh\ssh-key-2022-11-21.key") as sftp:
        print("Connection established.")

        remoteFilePath = "/var/www/website/static/sftp/images"
        localFilePath = fr"C:\src\projects\droneProject\meshroomBox\input\testGround"
        ## Check contents of the output folder
        dir = sftp.listdir()
        maxIdPlusOne = getMaxImageSetId() + 1
        newRemote = "/var/www/website/static/sftp/images/" + "imageset_" + str(maxIdPlusOne)
        print(newRemote)
        print(dir)
        ## Make a new directory in the folder to upload the model to
        sftp.execute("mkdir " + remoteFilePath + "/imageset_" + str(maxIdPlusOne))
        # Users other than ftp needs to be able to delete files so as a temp its just 777
        sftp.execute("chmod 777 " +  remoteFilePath + "/imageset_" + str(maxIdPlusOne))

        try:
            ## For every file in the output folder it uploads it to the server
            for file in os.listdir(localFilePath):
                print("Uploading file: " + file)
                sftp.put(localFilePath + "\\" + file, newRemote + "/" + file)
            #sftp.put(localFilePath, remoteFilePath)
            print("Files Uploaded")
            #print("Calling POST to server with image names for reference")
            #apiPostImages(imageJson)
        except Exception as e:
            print("Error")
            print(e)
        sftp.close()        
        # sftp.put_d('/home/rpi666/Desktop/cam_images','/ftpuser/eriksmappe/')  # upload file to public/ on remote
        # print("Data sent!")
        print("Closing SFTP connection.")



# def apiPostImageset(folderNumber):


# Saves the to the SQL database reference to the 3d model in a POST request to the API
def apiPostDoneModel():
    try:
        url = "http://"+ secrets["ip"] +":5000/savejob"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(exampleModelUploadJson), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"

def apiPostImages(jsonToSend):
    try:
        url = "http://"+ secrets["ip"] +":5000/saveimages"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(jsonToSend), headers=headers)
        return "Success"
    except Exception as e:
        print(e)
        return "Error"




# Saves images from dir into JSON file
def parseImagesToJson():
    global imageJson
    # Define the path to the directory containing the image files
    #image_dir = "C:\\path\\to\\directory\\with\\image\\files"
    image_dir = fr"C:\src\projects\droneProject\meshroomBox\input\testGround"

    # Get a list of the names of all the files in the directory
    file_names = os.listdir(image_dir)

    # Filter the list of file names to only include files with the desired image file extension (tupple with image names)
    image_names = [name for name in file_names if name.endswith((".jpg", ".JPG", ".png", ".PNG"))]

    # Define the JSON object that we will populate with data from the list of image file names

    # Iterate over the list of image file names and add each name to the "imageName" field of the JSON object
    for image_name in image_names:
        imageJson["imageName"].append(image_name)

    return imageJson

    # Print the resulting JSON object
    #print(imageJson)

# Edits the global json for imageupload
def editImageJson(id="1", token="1234567890", imageSetId = "3"):
    global imageJson
    imageJson = json.dumps(imageJson)
    jsonDict = json.loads(imageJson)
    jsonDict["userId"] = id
    jsonDict["imageSetId"] = imageSetId
    jsonDict["token"] = token
    imageJson = json.dumps(jsonDict)
    #print(json.load(imageJson))
    print(imageJson)




## Parses localhosts image folder to json incase we need to manually upload images 

# parseImagesToJson()
# editImageJson()
# apiPostImages(imageJson)
#print(imageJson)
#sftpUploadImages()


## Methods pipeline 

# Gets the jobs and saves the images to the imageNames list so it can be used in the sftpDownload method
# apigetjob()

# # Downloads the images from the sftp server
# sftpDownloadTest()

# # Runs the meshroom batch process
# MeshroomBatch()

# Uploads the rendered 3d model to the server
sftpUploadModel()

# POST request to rendered_model with reference to 3d model path



##Debug methods

# MeshroomBatchTest()
#sftpUploadTest()
#sftpDownloadTest()
#MeshroomBatch()
#apigetjob()
#sftpDownload()
#sftpUpload()

