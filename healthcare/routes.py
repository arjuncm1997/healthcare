import os 
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from healthcare import app,db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from healthcare.models import   AddDisease, DoctorAppoinment, TreatDisease, User, Quesions,Contact, Gallery
from healthcare.forms import RegistrationForm ,Resetrequest, DoctorRegistrationForm,Changepassword, LoginForm, Dquestions, Galleryform, Uprofileform, Dprofileform
from PIL import Image
import string
import random       
from random import randint                
from flask_mail import Message

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        new = Contact(usertype='public',name = name,email=email,phone=phone,subject=subject,message=message)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
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
        print(password)
        email = form.email.data
        sendemail(email,password)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new = User(username= form.username.data,email=form.email.data, specialisation = form.speci.data,address = form.address.data,password=hashed_password,phone = form.phone.data, usertype= 'doctor')
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/adddoctorview')

    else:
       return render_template('adddoctor.html',form=form)

def sendemail(email,password):
    msg = Message(' Online Health Care Registeration',
                  recipients=[email])
    msg.body = f'''  Your Password is, {password}  '''
    mail.send(msg)

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
    tasks=User.query.filter_by(usertype='doctor').all()
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
        diseases = AddDisease(owner = current_user.username,disease=disease,symptom=symptom,category=category,remedy=remedy)

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
    tasks = AddDisease.query.filter_by(owner=current_user.username).all()
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
        appoinments = DoctorAppoinment(owner=current_user.username ,name=name,doctor=doctor,reason=reason,contactno=contactno,date = date,status = '')

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
    gallery = Gallery.query.all()
    return render_template("gallery.html",gallery = gallery)

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

@app.route('/approveappoint/<int:id>')
def approveappoint(id):
    approve = DoctorAppoinment.query.get_or_404(id)
    approve.status = 'approved'
    db.session.commit()
    return redirect('/dappointments')


@app.route('/rejectappoint/<int:id>')
def rejectappoint(id):
    reject = DoctorAppoinment.query.get_or_404(id)
    reject.status = 'rejected'
    db.session.commit()
    return redirect('/dappointments')

@app.route('/dquestions',methods=['GET','POST'])
def dquestions():
    tasks = Quesions.query.filter_by(doctor=current_user.username).all()
    
    return render_template("dquestions.html",tasks = tasks)


@app.route('/dreply/<int:id>',methods=['GET','POST'])
def dreply(id):
    form = Dquestions()
    task = Quesions.query.get_or_404(id)
    if form.validate_on_submit():
        task.reply = form.reply.data
        db.session.commit() 
        return redirect('/dquestions')

    elif request.method == 'GET':
        form.reply.data = task.reply
    return render_template("dreply.html",form=form)
@app.route('/newdisease')
def newdisease():
     tasks = AddDisease.query.all()
     return render_template("newdisease.html",tasks = tasks)



@app.route('/ucontact',methods=['GET','POST'])
def ucontact():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        new = Contact(usertype='user',name = current_user.username,email=current_user.email,phone='',subject=subject,message=message)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/uindex')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('ucontact.html')


@app.route('/dcontact',methods=['GET','POST'])
def dcontact():
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        new = Contact(usertype = 'doctor',name = current_user.username,email=current_user.email,phone='',subject=subject,message=message)

        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/dindex')
        except:
            return 'There was an issue adding your task'

    else:
        return render_template('dcontact.html')



@app.route('/userfeedback')
def userfeedback():
    tasks = Contact.query.filter_by(usertype='user').all()
    return render_template("userfeedback.html",tasks = tasks)


@app.route('/publicfeedback')
def publicfeedback():
    tasks = Contact.query.filter_by(usertype='public').all()
    return render_template("publicfeedback.html",tasks = tasks)

@app.route('/doctorfeedback')
def doctorfeedback():
    tasks = Contact.query.filter_by(usertype='doctor').all()
    return render_template("doctorfeedback.html",tasks = tasks)

@app.route('/addgallery', methods=['GET','POST'])
def addgallery():
    form=Galleryform()
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            pic = pic_file

        new = Gallery(desc= form.desc.data,image =pic, )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/galleryview')
    return render_template('addgallery.html',title='Register', form=form)

@app.route('/galleryview')
def galleryview():
    tasks = Gallery.query.all()
    return render_template("galleryview.html",tasks = tasks)

@app.route('/gallerydelete/<int:id>')
def gallerydelete(id):
    delete = Gallery.query.get_or_404(id)

    try:
        db.session.delete(delete)
        db.session.commit()
        return redirect('/galleryview')
    except:
        return 'There was a problem deleting the task'

@app.route('/galleryupdate/<int:id>', methods=['GET', 'POST'])
def galleryupdate(id):
    form=Galleryform()
    pic = ""
    task = Gallery.query.get_or_404(id)
    if form.validate_on_submit():
        if form.image.data:
            pic_file = save_picture(form.image.data)
            task.image = pic_file
        task.desc = form.desc.data
        db.session.commit() 
        return redirect('/galleryview')
    elif request.method == 'GET':
        form.desc.data = task.desc
    return render_template("galleryupdate.html",form= form)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
@app.route('/userview')
def userview():
    tasks = User.query.filter_by(usertype='user').all()
    return render_template("userview.html",tasks =tasks)

@app.route('/uprofile/<int:id>',methods=['GET','POST'])
def uprofile(id):
    form = Uprofileform()
    task = User.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            view = save_picture(form.pic.data)
            task.image = view
        task.username = form.username.data
        task.email = form.email.data
        task.address = form.address.data
        task.phone = form.phone.data
        db.session.commit() 
        return redirect("")

    elif request.method == 'GET':
        form.username.data = task.username
        form.email.data = task.email
        form.address.data = task.address
        form.phone.data = task.phone
    return render_template("uprofile.html",form=form)


@app.route('/dprofile/<int:id>',methods=['GET','POST'])
def dprofile(id):
    form = Dprofileform()
    task = User.query.get_or_404(id)
    if form.validate_on_submit():
        if form.pic.data:
            view = save_picture(form.pic.data)
            task.image = view
        task.username = form.username.data
        task.email = form.email.data
        task.address = form.address.data
        task.phone = form.phone.data
        task.specialisation = form.speci.data
        db.session.commit() 
        return redirect("")

    elif request.method == 'GET':
        form.username.data = task.username
        form.email.data = task.email
        form.address.data = task.address
        form.phone.data = task.phone
        form.speci.data = task.specialisation
    return render_template("dprofile.html",form=form)




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form = Resetrequest()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/resetrequest')
    return render_template('resetrequest.html', title='Reset Password', form=form)

@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)

@app.route('/uchangepassword/<int:id>',methods=['GET','POST'])
@login_required
def uchangepassword(id):
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password changed please login again')
        return redirect('/uindex')
    return render_template("uchangepassword.html",form= form)


@app.route('/dchangepassword/<int:id>',methods=['GET','POST'])
@login_required
def dchangepassword(id):
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Password changed please login again')
        return redirect('/uindex')
    return render_template("dchangepassword.html",form= form)