import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskferrelli import app, db, bcrypt
from flaskferrelli.forms import CheckoutForm, RegistrationForm, LoginForm, UpdateAccountForm, ContactUsForm
from flaskferrelli.models import User, Rental
from flask_login import login_user, current_user, logout_user, login_required

#route declarators for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#route declarator for about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')

#route declarator for contact us page
@app.route("/contactus", methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactUsForm()
    if form.validate_on_submit():
        flash('Your Comment Has Been Submitted', 'success')
        return redirect(url_for('contact'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('contactus.html', title='Contact Us', form=form)

#route declarator for collection page
@app.route("/collection")
def collection():
    return render_template('collection.html', title='Collection')

#route declarator for register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    #check for validation 
    if form.validate_on_submit():
        #create a hashed password using Flask Bcrypt class and decode to utf-8
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #user variable
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        #add and commit user to db
        db.session.add(user)
        db.session.commit()
        #flask flash alert and bootstrap class for "success" alert style
        flash(f'Your account has been created! Please log in now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#route declarator for login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #check for validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Login attempt unsuccessful. Please try again', 'danger')
    return render_template('login.html', title='Login', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images_profile', picture_fn)
    
    # output_size = (125, 125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)

    form_picture.save(picture_path)

    return picture_fn

#route declarator for profile page
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    #update username and email to db after validate_on_submit
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        #flash('Your account has been updated!', 'danger')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        if current_user.rental:
            form.rental.data = current_user.rental
        else:
            form.rental.data = 'No Current Rental'
    image_file = url_for('static', filename='images_profile/' + current_user.image_file)
    return render_template('profile.html', title='Profile', image_file=image_file, form=form)

#orm = object relational mapper (SQLAlchemy)

#route declarator for logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#route declarator for checkout page
@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        if current_user.rental:
            flash('You can only rent one car at a time', 'danger')
            return redirect(url_for('collection'))
        else:
            rental = Rental(year=form.year.data, makemodel=form.makemodel.data,
                            startdate=form.startdate.data, enddate=form.enddate.data,
                            user_id = current_user.id)
            db.session.add(rental)
            db.session.commit()
            flash('Your payment has been approved to experience the drive of your dreams!', 'success')
            return redirect(url_for('collection'))
    elif request.method == 'GET':
        year = request.args.get('year')
        makemodel = request.args.get('makemodel')
        price = request.args.get('price')
        form.year.data = year
        form.makemodel.data = makemodel
        form.price.data = '$' + price + ' per day plus $30 per mile' 
    return render_template('checkout.html', title='Profile', form=form)