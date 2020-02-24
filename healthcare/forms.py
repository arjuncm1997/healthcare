from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from healthcare.models import  AddDisease, DoctorAppoinment, TreatDisease, User
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import SelectField



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=1, max=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),Length(min=1, max=8) ,EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class DoctorRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    speci = StringField('Specilisation',
                           validators=[Length(min=2, max=20)])
    address = StringField('Address',
                           validators=[Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[Length(min=2, max=20)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')  

class Dquestions(FlaskForm):
    reply = TextAreaField('reply',
                           validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submitt')


class Galleryform(FlaskForm):
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    desc = StringField('Description',
                           validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submitt')

class Uprofileform(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')

class Dprofileform(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    
    address = StringField('Address',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=20)])
    speci = StringField('Specilisation',validators=[Length(min=2, max=20)])
    submit = SubmitField('Submit')


class Resetrequest(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class Changepassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),Length(min=1, max=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),Length(min=1, max=8) ,EqualTo('password')])
    submit = SubmitField('Reset')