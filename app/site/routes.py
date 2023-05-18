from flask import Blueprint, render_template, flash, redirect, url_for, request
from forms import  AddMemeForm, UpdateAccountForm
from models import  Meme, db
from flask_login import current_user, login_required
from helpers import save_picture


site = Blueprint('site', __name__, template_folder = 'site_templates')


@site.route('/')
@site.route('/home')
def home():
    memes = Meme.query.all()
    return render_template('home.html', pics = memes)





@site.route('/add_meme', methods = ['GET','POST'])
@login_required
def add_meme():
    form = AddMemeForm()
    if form.validate_on_submit():
        meme_file = save_picture(form.picture.data, 'meme_photos')
        meme = Meme(meme_file, current_user.token, form.public.data)
        db.session.add(meme)
        db.session.commit()
        flash('You have succesfully added a meme to your collection', 'success')
        return redirect(url_for('site.home'))
    return render_template('meme.html', form = form)
    


@site.route('/account', methods = ["GET", 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
                
            picture_file = save_picture(form.picture.data, 'profile_pics')
            current_user.profile_photo = picture_file


        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('site.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_photo = url_for('static', filename = 'profile_pics/' + current_user.profile_photo)
    return render_template('account.html', image_file = profile_photo, form = form)

