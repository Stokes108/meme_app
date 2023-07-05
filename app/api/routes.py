from flask import Blueprint, request, jsonify, render_template, json
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema
from flask_login import current_user
from helpers import save_picture, delete_picture


api = Blueprint('api', __name__, url_prefix = '/api', template_folder= 'api_templates')






@api.route('/memes', methods= ['POST'])
@token_required
def create_meme(current_token):

    # file = open(app.root_path)

    # e = MultipartEncoder({'upload[file]': (file.name, file, 'application/octet-stream'),
    # 'upload[active]': 'True',
    # 'upload[title]': 'Title From Python - Monitored with bar'})

    #  payload = MultipartEncoderMonitor(e)


    # url = f'http://127.0.0.1:5000/api/memes{current_token.token}'
    given_file = request.json['file']
    meme_file = save_picture(given_file, 'meme_photos')
    public = request.json['public']
    content_top = request.json['content_top']
    content_bottom = request.json['content_bottom']
    user_token = current_token.token

    print(type(public))
    print(public)


    print(type(public))
    print(f'BIG TESTER: {current_token.token}')

    meme = Meme(meme_file, content_top = content_top, content_bottom = content_bottom, user_token = user_token, public = public)
    db.session.add(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)

#display all cars
@api.route('/memes', methods= ['GET'])
@token_required
def display_cars(current_token):
    user = current_token.token
    memes = Meme.query.filter_by(user_token = user).all()
    response = memes_schema.dump(memes)
    return jsonify(response)

# display a single car
@api.route('/meme/<id>', methods= ['GET'])
@token_required
def get_single_car(current_token, id):
    meme = Meme.query.get(id)
    response = meme_schema.dump(meme)
    return jsonify(response)


#update a particular car
@api.route('meme/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_token, id):
   meme = Meme.query.get(id)
   meme.content_top = request.json['content_top']
   meme.content_bottom = request.json['content_bottom']
   print(request.json['content_top'])

#    meme.picture = request.json['picture']
   meme.user_token = current_token.token

   db.session.commit()
   response = meme_schema.dump(meme)
   return jsonify(response)

# deleates a particular meme
@api.route('/meme/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_token, id):

    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()

    delete_picture(meme, 'meme_photos')

    
    response = meme_schema.dump(meme)
    return jsonify(response)



#create a collection route 
#create an all memes route
