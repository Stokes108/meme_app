from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime
from flask_login import UserMixin, LoginManager
import uuid 

from werkzeug.security import generate_password_hash, check_password_hash

import secrets

from flask_marshmallow import Marshmallow 

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String(150), unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    profile_photo = db.Column(db.String(30), nullable = False)
    memes = db.relationship('Meme', back_populates='owner', lazy='subquery')

    def __init__(self, username, email, password, profile_photo, token = ''):
        self.username = username
        self.email = email
        self.profile_photo = profile_photo
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash
    
    def set_id(self):
        return int(uuid.uuid4())

    
    def __repr__(self):
        return f'User {self.username} with {self.email} is in the Database'
    




class Meme(db.Model):
    id = db.Column(db.String, primary_key = True)
    content = db.Column(db.Text, nullable = False, default='')
    image_file = db.Column(db.String(100), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'),nullable = False)
    public = db.Column(db.Boolean, nullable = False, default = False)
    owner = db.relationship('User' , back_populates ='memes')

    def __init__ (self, image_file, user_token, public ,content = 'This is your meme!!!!'):
        self.id = self.set_id()
        self.content = content
        self.public = public
        self.image_file = image_file
        self.user_token = user_token
    
    def set_id(self):
        return (secrets.token_urlsafe())
    

    def __repr__(self):
        return f'The meme {self.id} is here!'
 
class MemeSchema(ma.Schema):
    class Meta:
        fields  = ['id', 'content', 'image_file', 'public']

meme_schema = MemeSchema()
memes_schema = MemeSchema(many = True)
