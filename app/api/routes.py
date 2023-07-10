from flask import Blueprint, request, jsonify, render_template, json
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema, PictureState
from flask_login import current_user
from helpers import save_picture, delete_picture



api = Blueprint('api', __name__, url_prefix = '/api', template_folder= 'api_templates')

pic = PictureState()


@api.route('/memes-picture', methods= ['GET'])
@token_required
def get_pic_path(current_token):
    print(pic.pic_path)
    pic_dict = {'pic_path': pic.pic_path}
    return jsonify(pic_dict)



@api.route('/memes-picture', methods= ['POST'])
@token_required
def save_meme_picture(current_token):
    given_file = request.files['file']
    meme_file = save_picture(given_file, 'meme_photos')
    pic.setPic(meme_file)
    print(pic.pic_path)
    return jsonify(meme_file)


@api.route('/memes', methods= ['POST'])
@token_required
def create_meme(current_token):


    meme_pic = request.json['file']
    content_top = request.json['content_top']
    content_bottom = request.json['content_bottom']
    public = request.json['public']

    user_token = current_token.token




    print(f'BIG TESTER: {current_token.token}')

    meme = Meme(meme_pic, content_top = content_top, content_bottom = content_bottom, public=public, user_token = user_token)
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
