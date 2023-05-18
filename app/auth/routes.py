from flask import Blueprint, render_template, flash, redirect, url_for, request
from models import User, check_password_hash, db
from flask_login import login_user, current_user, logout_user, login_required
from forms import RegisterForm, LoginForm


auth = Blueprint('auth', __name__, template_folder = 'auth_templates')


@auth.route('/login', methods = ["GET", 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('site.home'))
        else:
            flash(f'Login Unsuccessful for {form.email.data}. Please check email and password', 'danger')
    return render_template('login.html', form = form)





@auth.route('/register', methods = ["GET", 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.home'))
    
    form = RegisterForm()
    if form.validate_on_submit():


        user = User(username = form.username.data, email = form.email.data, password = form.password.data, profile_photo = form.pic.data)
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')

        return redirect(url_for('auth.login'))
    return render_template('register.html', form = form)


@auth.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
