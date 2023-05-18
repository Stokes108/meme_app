from flask import Flask
from config import Config
import os
from PIL import Image
import secrets

from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS


app = Flask(__name__)


CORS(app)


app.config.from_object(Config)

root_db.init_app(app)
login_manager.init_app(app)

ma.init_app(app)
migrate = Migrate(app, root_db)

from helpers import JSONEncoder
app.json_encoder = JSONEncoder







def save_picture(form_picture, folder):

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

def delete_picture(meme, folder):
    picture_path = os.path.join(app.root_path, f'static/{folder}', meme.image_file)
    os.remove(picture_path)


from .auth.routes import auth
from .site.routes import site
from .api.routes import api


app.register_blueprint(auth)
app.register_blueprint(site)
app.register_blueprint(api)

