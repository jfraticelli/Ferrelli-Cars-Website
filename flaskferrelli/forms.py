from ast import Num
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flaskferrelli.models import User

#registration form class inherits FlaskForm 
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken')

#login form class inherits FlaskForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

#update account form class inherits FlaskForm 
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rental = StringField('Current Rental')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpeg','png','webp'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken')

#contact us form class inherits FlaskForm
class ContactUsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Leave a comment or concern here', validators=[DataRequired()])
    submit = SubmitField('Submit')

#checkout form class inherits FlaskForm
class CheckoutForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1990, max=2022)])
    makemodel = StringField('Make/Model', validators=[DataRequired()])
    price = StringField('Total Cost', validators=[DataRequired()])
    creditcard = IntegerField('Credit Card Number', validators=[DataRequired(), NumberRange(min=1000000000000000, max=9999999999999999)])
    startdate = DateField('Rental Date: ', format='%Y-%m-%d', validators=[DataRequired()])
    enddate = DateField('Return Date: ', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Rent Now')
