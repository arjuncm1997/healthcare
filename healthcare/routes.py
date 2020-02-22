import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from healthcare import app,db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from healthcare.models import   AddDisease, DoctorAppoinment, TreatDisease, User, Quesions
from healthcare.forms import RegistrationForm , DoctorRegistrationForm, LoginForm, Dquestions
from PIL import Image
import string
import random                       


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, usertype= 'user' ).first()
        user1 = User.query.filter_by(email=form.email.data, usertype= 'doctor').first()
        user2 = User.query.filter_by(email=form.email.data, usertype= 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/dindex')
        if user2 and user2.password== form.password.data:
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
        if user2 and bcrypt.check_password_hash(user2.password, form.password.data):
            login_user(user2, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new = User(username= form.username.data,email=form.email.data, password=hashed_password, usertype= 'user')
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('register.html',title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')
    

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/adddoctor', methods=['GET',"POST"])
def adddoctor():
    form=DoctorRegistrationForm()
    if form.validate_on_submit():
        def randomString(stringLength=10):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(stringLength))
        password =randomString()
        new = User(username= form.username.data,email=form.email.data, specialisation = form.speci.data,address = form.address.data,password=password,phone = form.phone.data, usertype= 'doctor')
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/adddoctorview')

    else:
       return render_template('adddoctor.html',form=form)

@app.route('/aeditdoctor/<int:id>', methods=['GET', 'POST'])
def aeditdoctor(id):
    form=DoctorRegistrationForm()
    task = User.query.get_or_404(id)
    if form.validate_on_submit():
        task.username = form.username.data
        task.email = form.email.data
        task.specialisation = form.speci.data
        task.address = form.address.data
        task.phone = form.phone.data
        db.session.commit() 
        return redirect('/adddoctorview')
    elif request.method == 'GET':
        form.username.data = task.username
        form.email.data = task.email
        form.speci.data = task.specialisation
        form.address.data = task.address
        form.phone.data = task.phone
    return render_template("aeditdoctor.html",form= form)





@app.route('/adddoctorview')
def adddoctorview():
    tasks=User.query.all()
    return render_template('adddoctorview.html',tasks=tasks)

@app.route('/adddoctordelete/<int:id>')
def adddoctordelete(id):
    delete = User.query.get_or_404(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/adddoctorview')
    except:
        return 'There was a problem deleting the task'


@app.route('/adddisease',methods=['GET','POST'])
def adddisease():
    if request.method == 'POST':
        disease = request.form['disease']
        symptom = request.form['symptom']
        category = request.form['category']
        remedy = request.form['remedy']
        diseases = AddDisease(disease=disease,symptom=symptom,category=category,remedy=remedy)

        try:
            db.session.add(diseases)
            db.session.commit()
            return redirect('/adddiseaseview')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('adddisease.html')

@app.route('/adddiseaseview')
def adddiseaseview():
    tasks = AddDisease.query.all()
    return render_template('adddiseaseview.html',tasks=tasks)

@app.route('/adddiseasedelete/<int:id>')
def adddiseasedelete(id):
    task_to_delete = AddDisease.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/adddiseaseview')
    except:
        return 'There was a problem deleting the task'



@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/doctorappoinment',methods=['GET','POST'])
def doctorappoinment():
    doctor = User.query.filter_by(usertype='doctor').all()
    if request.method == 'POST':
        name = request.form ['name']
        doctor = request.form ['doctor']
        reason = request.form ['reason']
        contactno = request.form ['contactno']
        date = request.form ['date']
        appoinments = DoctorAppoinment(owner=current_user.username ,name=name,doctor=doctor,reason=reason,contactno=contactno,date = date)

        try:
            db.session.add(appoinments)
            db.session.commit()
            return redirect('/doctorappoinmentview')

        except:
            return 'There was an issue adding your task'
    
    else:
        return render_template('doctorappoinment.html',doctor=doctor)

@app.route('/doctorappoinmentview')
def doctorappoinmentview():
    tasks= DoctorAppoinment.query.filter_by(owner=current_user.username).all()
    return render_template('doctorappoinmentview.html',tasks=tasks)

@app.route('/doctorappoinmentdelete/<int:id>')
def doctorappoinmentdelete(id):
    task_to_delete = DoctorAppoinment.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/doctorappoinmentview')
    except:
        return 'There was a problem deleting that task'

@app.route('/treatdisease',methods=['GET','POST'])
def treatdisease():
    if request.method == 'POST':
        name = request.form ['name']
        location = request.form ['location']
        disease = request.form ['disease']
        contactno = request.form ['contactno']
        treatment = TreatDisease(name=name,location=location,disease=disease,contactno=contactno)

        try:
            db.session.add(treatment)
            db.session.commit()
            return redirect('/treatdiseaseview')

        except:
            return 'There was an issue adding your task'
    
    else:
        return render_template('treatdisease.html')

@app.route('/treatdiseaseview')
def treatdiseaseview():
    tasks= TreatDisease.query.all()
    return render_template('treatdiseaseview.html',tasks=tasks)

@app.route('/treatdiseasedelete/<int:id>')
def treatdiseasedelete(id):
    task_to_delete = TreatDisease.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/treatdiseaseview')
    except:
        return 'There was a problem deleting that task'


@app.route('/uindex')
@login_required
def uindex():
    return render_template('uindex.html')

@app.route('/gallery')
def gallery():
    return render_template("gallery.html")

@app.route('/udoctor')
def udoctor():
    return render_template("udoctor.html")

@app.route('/uquestion')
def uquestion():
    return render_template("uquestion.html")

@app.route('/dindex')
@login_required
def dindex():
    return render_template("dindex.html")

@app.route('/ddisease')
def ddisease():
    return render_template("ddisease.html")


@app.route('/uask',methods=['GET','POST'])
def uask():
    doctor = ""
    doctor = User.query.filter_by(usertype='doctor').all()
    if request.method == 'POST':
        name = request.form['name']
        question = request.form['question']
        doctor = request.form['doctor']
        new = Quesions(owner = current_user.username,name =name ,question = question,doctor = doctor,reply='')

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/uindex')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template("uask.html", doctor = doctor )


@app.route('/uaskview')
def uaskview():
    task = Quesions.query.filter_by(owner=current_user.username).all()
    return render_template("uaskview.html",tasks=task)

@app.route('/uaskdelete/<int:id>')
def uaskdelete(id):
    delete = Quesions.query.get_or_404(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/uaskview')
    except:
        return 'There was a problem deleting that task'


@app.route('/dappointments')
def dappointments():
    tasks= DoctorAppoinment.query.filter_by(doctor=current_user.username).all()
    return render_template("dappointments.html",tasks=tasks)


@app.route('/dquestions')
def dquestions():
    form = Dquestions()
    tasks = Quesions.query.filter_by(doctor=current_user.username).all()
    return render_template("dquestions.html",tasks = tasks,form=form)