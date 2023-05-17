from flask import Blueprint, request, jsonify, render_template, json
from helpers import token_required
from models import db, User, Meme, meme_schema, memes_schema
from flask_login import current_user
from helpers import save_picture


api = Blueprint('api', __name__, url_prefix = '/api', template_folder= 'api_templates')






@api.route('/memes', methods= ['POST'])
@token_required
def create_meme(current_token):
    given_file = request['file']
    meme_file = save_picture(given_file, 'meme_photos')
    public = request.json['public']
    user_token = current_token.token

    print(type(public))
    print(public)


    print(type(public))
    print(f'BIG TESTER: {current_token.token}')

    meme = Meme(meme_file, user_token = user_token, public = public)
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
@api.route('/car/<id>', methods= ['GET'])
@token_required
def get_single_car(current_token, id):
    meme = Meme.query.get(id)
    response = meme_schema.dump(meme)
    return jsonify(response)


#update a particular car
@api.route('cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_token, id):
   meme = Meme.query.get(id)
   meme.content = request.json['content']
   meme.picture = request.json['picture']
   meme.user_token = current_token.token

   db.session.commit()
   response = meme_schema.dump(meme)
   return jsonify(response)

# deleates a particular car
@api.route('/car/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)



#create a collection route 
#create an all memes route
