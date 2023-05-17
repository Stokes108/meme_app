from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal 
import os
from PIL import Image
from models import User
from meme_app import app

def token_required(our_flask_func):
    @wraps(our_flask_func)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message' : 'Token is missing.'})
        
        try:
            current_token = User.query.filter_by(token = token).first()
        except:
            owner = User.query.filter_by(token = token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid.'})
        
        return our_flask_func(current_token, *args, **kwargs)
    return decorated


def save_picture(form_picture, folder):
    print(os.getcwd())
    # basedir = os.path(os.path.dirname(__file__))



    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/{folder}', picture_fn)
    
    i = Image.open(form_picture)

    if folder == 'profile_pics':
        output_size = (125, 125)
        i.thumbnail(output_size)    
    i.save(picture_path)

    return picture_fn

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

                                                        