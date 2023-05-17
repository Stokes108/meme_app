# from flask import Flask, render_template, flash, redirect, url_for, request
# from forms import LoginForm, RegisterForm, AddMemeForm, UpdateAccountForm
# from models import User, Meme, check_password_hash
# from flask_login import login_user, current_user, logout_user, login_required
# import secrets
# import os
# from PIL import Image


# site = Blueprint('site', __name__, template_folder = 'site_templates')


# @site.route('/')
# @site.route('/home')
# def home():
#     memes = Meme.query.all()
#     return render_template('home.html', pics = memes)



# @site.route('/login', methods = ["GET", 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email = form.email.data).first()

#         if user and check_password_hash(user.password, form.password.data):
#             login_user(user, remember = form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash(f'Login Unsuccessful for {form.email.data}. Please check email and password', 'danger')
#     return render_template('login.html', form = form)


# @site.route('/register', methods = ["GET", 'POST'])
# def register():

#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
    
#     form = RegisterForm()
#     if form.validate_on_submit():


#         user = User(username = form.username.data, email = form.email.data, password = form.password.data, profile_photo = form.pic.data)
#         db.session.add(user)
#         db.session.commit()

#         flash(f'Your account has been created! You are now able to log in', 'success')

#         return redirect(url_for('login'))
#     return render_template('register.html', form = form)


# @site.route('/logout', methods = ['GET'])
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# def save_picture(form_picture, folder):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, f'static/{folder}', picture_fn)
    
#     i = Image.open(form_picture)

#     if folder == 'profile_pics':
#         output_size = (125, 125)
#         i.thumbnail(output_size)    
#     i.save(picture_path)

#     return picture_fn

# @app.route('/add_meme', methods = ['GET','POST'])
# @login_required
# def add_meme():
#     form = AddMemeForm()
#     if form.validate_on_submit():
#         meme_file = save_picture(form.picture.data, 'meme_photos')
#         meme = Meme(meme_file, current_user.token, form.public.data)
#         db.session.add(meme)
#         db.session.commit()
#         flash('You have succesfully added a meme to your collection', 'success')
#         return redirect(url_for('home'))
#     return render_template('meme.html', form = form)
    


# @app.route('/account', methods = ["GET", 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()

#     if form.validate_on_submit():
#         picture_file = save_picture(form.picture.data, 'profile_pics')
#         current_user.profile_photo = picture_file


#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('account'))
    
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     profile_photo = url_for('static', filename = 'profile_pics/' + current_user.profile_photo)
#     return render_template('account.html', image_file = profile_photo, form = form)


# from flask import Blueprint, request, jsonify, render_template, json
# from helpers import token_required
# from models import db, User, Car, car_schema, cars_schema
# from flask_login import current_user


# @api.route('/cars', methods= ['POST'])
# @token_required
# def create_car(current_token):
#     make = request.json['make']
#     model = request.json['model']
#     year = request.json['year']
#     color = request.json['color']
#     user_token = current_token.token

#     print(f'BIG TESTER: {current_token.token}')

#     car = Car(make, model, year, user_token, color)

#     db.session.add(car)
#     db.session.commit()

#     response = car_schema.dump(car)
#     return jsonify(response)

# # retrieve all the cars
# @api.route('/displaycars')
# def display():

#     return render_template('display.html', title ='Your Cars', cars = current_user.cars)

#     user = current_token.token
#     cars = Car.query.filter_by(user_token = user).all()
#     response = cars_schema.dump(cars)
#     return jsonify(response)

# #display all cars
# @api.route('/cars', methods= ['GET'])
# @token_required
# def display_cars(current_token):
#     user = current_token.token
#     cars = Car.query.filter_by(user_token = user).all()
#     response = cars_schema.dump(cars)
#     return jsonify(response)

# # display a single car
# @api.route('/car/<id>', methods= ['GET'])
# @token_required
# def get_single_car(current_token, id):
#     car = Car.query.get(id)
#     response = car_schema.dump(car)
#     return jsonify(response)


# #update a particular car
# @api.route('cars/<id>', methods = ['POST', 'PUT'])
# @token_required
# def update_car(current_token, id):
#    car = Car.query.get(id)
#    car.make = request.json['make']
#    car.model = request.json['model']
#    car.year = request.json['year']
#    car.color= request.json['color']
#    car.user_token = current_token.token

#    db.session.commit()
#    response = car_schema.dump(car)
#    return jsonify(response)

# @api.route('/car/<id>', methods = ['DELETE'])
# @token_required
# def delete_car(current_token, id):
#     car = Car.query.get(id)
#     db.session.delete(car)
#     db.session.commit()

#     response = car_schema.dump(car)
#     return jsonify(response)



# #create a collection route 
# #create an all memes route
