from healthcare import db, app, login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):

    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(80), nullable=False)
    specialisation = db.Column(db.String(300))
    image= db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)



class AddDisease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.VARCHAR(200), nullable=False)
    symptom = db.Column(db.VARCHAR(200), nullable=False)
    category = db.Column(db.VARCHAR(200), nullable=False)
    remedy = db.Column(db.VARCHAR(200), nullable=False)

class DoctorAppoinment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String)
    name = db.Column(db.VARCHAR(200), nullable=False)
    doctor = db.Column(db.VARCHAR(200), nullable=False)
    reason = db.Column(db.VARCHAR(200), nullable=False)
    contactno = db.Column(db.VARCHAR(200), nullable=False)
    date = db.Column(db.VARCHAR(200), nullable=False)
    status = db.Column(db.String(200), nullable=False)

class TreatDisease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(200), nullable=False)
    location = db.Column(db.VARCHAR(200), nullable=False)
    disease = db.Column(db.VARCHAR(200), nullable=False)
    contactno = db.Column(db.VARCHAR(200), nullable=False)


class Quesions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(200),nullable=False)
    name = db.Column(db.String(200), nullable=False)
    reply = db.Column(db.String(200), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    doctor = db.Column(db.String(200), nullable=False)