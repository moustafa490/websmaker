from flask import Flask, render_template, redirect, session, request, flash
from services.models import *
from flask_cors import CORS
import os

from email.message import EmailMessage
import ssl
import smtplib

PORT = 5000
DB_FILENAME = 'database.db'
INIT_DB = True  # to create db file


app = Flask(__name__)


def create_app():
   
    # create flask app
    app = Flask(__name__)

    # create database extension
    app.secret_key = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + DB_FILENAME

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    # create flask cors extension
    CORS(app)
    with app.app_context():
        db.create_all()
    return app, db


# create flask app
app, db = create_app()

####################


###############

@app.route('/' )
def index():
    return render_template('index.html')

'''
@app.route('/sendmail', methods=['POST'])
def send_email():
    email_sender = 'coursesforyo@gmail.com'
    email_password = 'hthaynywgefenetz'
    email_receiver = request.form.get('email')
    subject = request.form.get('subject')
    body = request.form.get('message')
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = "moustafasamy490@gmail.com"
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp :
        smtp.login(email_sender , email_password)
        smtp.sendmail(email_sender , email_receiver , em.as_string())
    return redirect('/')
    
'''

@app.route('/sendmail', methods=['POST'])
def send_email():
    name =request.form.get("name")
    email = request.form.get('email')
    ##
    email_sender = 'coursesforyo@gmail.com'
    email_password = 'hthaynywgefenetz'
    email_receiver = "websmakersite@gmail.com"
    subject =  request.form.get('subject')
    body =  request.form.get('message')
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(" From "+ name +"\n"+" Message is  :"+"\n" + body+"\t \n"+"sender email is : \n"+email)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp :
        smtp.login(email_sender , email_password)
        smtp.sendmail(email_sender , email_receiver , em.as_string())

    
    message=messages(name = name,email = email,message= body,subject= subject )
    db.session.add(message)
    db.session.commit()
    return redirect('/')
    
############ ADMIN#########

@app.route('/loginiamadmin')
def Get_login():
    return render_template('login.html')

@app.route('/loginiamadmin' , methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')

    query = meAdmin.check_username(username)
    if( query != None ):
        
        if query.password != password:
        # @TODO return a proper failure message
            return "<h1>wrong password</h1>"
        flash("logged in successfully")
             # save session
        print("LOGIN success")
        session.permanent = True
        session['myisadmin'] = username
        session['myisadmin'] = True
        return redirect('/')
    return "wrong username"

@app.route('/panal')
def Get_panal():
    if "myisadmin" in session:
        ms = messages.query.all()
        return render_template('panal.html' , ms = ms)
    else:
        return"CANT ACCESS"
#######################################################################################logout##############################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
    ################ wrong route ################

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
#########################################################to run the website####################################################################
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')