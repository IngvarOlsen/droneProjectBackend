from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import Table, select, join, MetaData
#from .models import Note, ImageSet, Image
from .models import ImageSet, Image, RenderedModel, Job
from . import db #, session
import json
import os
#Import apy.py
from . import api
import collections



views = Blueprint('views', __name__)

@views.route('/sftp/<filename>')
def serve_file(filename):
    return send_from_directory('/var/www/sftp', filename)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    cwd = os.getcwd()
    print(cwd)

    
    imageSets = api.getImages(str(current_user.id))
    print(imageSets)
    ## Convert the SQL data to json so each got a key and value
    # objects_list = []
    # for image in imageSets:
    #     d = collections.OrderedDict()
    #     d['image_set_id'] = image[0][4]
    #     #d['image_name'] = image[2]
    #     objects_list.append(d)

    # imagesJson = json.dumps(objects_list)
    # print(imagesJson)



    ## Gets all users imagesets and images in a SQL Query and dumps it to json
    # imageSets = ImageSet.query.filter_by(user_id=current_user.id).all()
    # for images in imageSets:
    #     images = Image.query.filter_by(imageset_id=imageSet.id).all()
    #     images.images = images
    # print(json.dump(images))
    

    # imageSets = os.listdir('website/static/imagesets')
    # imageSets = ['imagesets/' + file for file in imageSets]
    ## image sorting by start image name id into different lists in a dictionary
    # imageSetsList = []
    # for imageSet in imageSets:
    #     imageSetId = imageSet.split('_')[0]
    #     if imageSetId not in imageSetsList:
    #         imageSetsList[imageSetId] = [imageSetId]
    #     imageSetsList.append(imageSet)
    # print(imageSetsList)

    # imageSetsDict = {}
    # for imageSet in imageSets:
    #     imageSetId = imageSet.split('_')[0]
    #     if imageSetId not in imageSetsDict:
    #         imageSetsDict[imageSetId] = []
    #     imageSetsDict[imageSetId].append(imageSet)
    # print(imageSetsDict)

    # ## Splitting up dictionary into lists
    # imageSetsList = []
    # for key, value in imageSetsDict.items():
    #     imageSetsList.append(value)
    # print(imageSetsList)

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

    ##return render_template("home.html", user=current_user, imageSetsList = imageSetsList)
    return render_template("home.html", user=current_user, imageSets = imageSets)





# @views.route('/renders', methods=['GET', 'POST'])
# @login_required
# def renders():
#     cwd = os.getcwd()
#     print(cwd)

#     ## Gets all Jobs from the Job table 
#     print(current_user.id)
#     rendersData = api.getRenders(str(current_user.id))
#     print(rendersData)

#     ##return render_template("home.html", user=current_user, imageSetsList = imageSetsList)
#     return render_template("renders.html", user=current_user, jobs = rendersData)





@views.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    cwd = os.getcwd()
    print(cwd)
    print(current_user.id)
    ## Gets all Jobs from the Job table 
    jobsData = api.getJobs(str(current_user.id))



    
    # imageSets = api.getImages(str(current_user.id))
    # print(imageSets)
    ## Gets all Jobs from the Job table in sqlalchemy
    # jobsData = Job.query.filter_by(user_id=current_user.id).all()
    # print(jobsData[0].status)
    # #metadata = MetaData(bind=db)
    # # Define the Table objects for each table in the database
    # job = Table('Job', session, autoload=True)
    # renderedModel = Table('RenderedModel', session, autoload=True)
    # # Build a query to select all columns from job and renderedModel
    # # where the values in the `id` column of job and the `job_id`
    # # column of renderedModel are equal
    # query = select([job, renderedModel]).where(job.columns.user_id == renderedModel.columns.user_id)
    # # Use the `select_from()` method to specify the join as the source
    # # for the data you want to select
    # query = query.select_from(join(job, renderedModel))
    # # Execute the query and fetch the results
    # results = db.execute(query).fetchall()
    # # Iterate over the results and print the values in each row
    # for row in results:
    #     print(row[job.columns.col1], row[renderedModel.columns.col2])



    ##return render_template("home.html", user=current_user, imageSetsList = imageSetsList)
    return render_template("jobs.html", user=current_user, jobs = jobsData)

@views.route('/renders', methods=['GET', 'POST'])
@login_required
def renders():
    print(current_user.id)
    ## Gets all Jobs from the Job table 
    rendersData = api.getRenders(str(current_user.id), "1234567890")
    print(rendersData)

    ##return render_template("home.html", user=current_user, imageSetsList = imageSetsList)
    return render_template("renders.html", user=current_user, renders = rendersData)

@views.route('/renderview/<id>', methods=['GET'])
@login_required
def renderView(id):
    print("id is: " + id)
    renderData = api.getRenderById(str(id))
    # Prints out the render data json.loads object
    print(renderData[0][1])
    

    ##return render_template("home.html", user=current_user, imageSetsList = imageSetsList)
    return render_template("renderview.html", user=current_user, path = renderData[0][1])





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
# @views.route('/get-imagesets', methods=['GET'])
# def get_imagesets():
#     imageSets = ImageSet.query.all()
#     imageSets = [imageSet.serialize() for imageSet in imageSets]
#     return jsonify(imageSets)
    



