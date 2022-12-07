from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from .models import Note, ImageSet, Image
from .models import ImageSet, Image, RenderedModel
from . import db
import json
import os

views = Blueprint('views', __name__)

@views.route('/sftp/<filename>')
def serve_file(filename):
    return send_from_directory('/var/www/sftp', filename)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    cwd = os.getcwd()
    print(cwd)
    imageSets = os.listdir('website/static/imagesets')
    imageSets = ['imagesets/' + file for file in imageSets]


    ## image sorting by start image name id into different lists in a dictionary
    # imageSetsList = []
    # for imageSet in imageSets:
    #     imageSetId = imageSet.split('_')[0]
    #     if imageSetId not in imageSetsList:
    #         imageSetsList[imageSetId] = [imageSetId]
    #     imageSetsList.append(imageSet)
    # print(imageSetsList)

    imageSetsDict = {}
    for imageSet in imageSets:
        imageSetId = imageSet.split('_')[0]
        if imageSetId not in imageSetsDict:
            imageSetsDict[imageSetId] = []
        imageSetsDict[imageSetId].append(imageSet)
    print(imageSetsDict)

    ## Splitting up dictionary into lists
    imageSetsList = []
    for key, value in imageSetsDict.items():
        imageSetsList.append(value)
    print(imageSetsList)

    # imageSetsDict = {}
    # for imageSet in imageSets:
    #     startImage = imageSet.split('_')[0]
    #     if startImage in imageSetsDict:
    #         imageSetsDict[startImage].append(imageSet)
    #         print(imageSetsDict)
    #     else:
    #         imageSetsDict[startImage] = [imageSet]
    #         print(imageSetsDict)
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Note added!', category='success')

    return render_template("home.html", user=current_user, imageSetsList = imageSetsList)


@views.route('/authtest', methods=['GET', 'POST'])
# @login_required
def authTest():
    return render_template("authtest.html", user=current_user)

@views.route('/renderviewtest', methods=['GET', 'POST'])
# @login_required
def renderViewTest():
    return render_template("renderviewtest.html", user=current_user)


############# API #############

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})


## Returns a json with the SELECT all imagesets from the database
@views.route('/get-imagesets', methods=['GET'])
def get_imagesets():
    imageSets = ImageSet.query.all()
    imageSets = [imageSet.serialize() for imageSet in imageSets]
    return jsonify(imageSets)
    



