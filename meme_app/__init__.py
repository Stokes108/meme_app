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







from .auth.routes import auth
from .site.routes import site
from .api.routes import api


app.register_blueprint(auth)
app.register_blueprint(site)
app.register_blueprint(api)

