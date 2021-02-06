import os
from flask import Flask
# from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
# from flask_mysqldb import MySQL
# from flask_session import Session
# from flask_mail import Mail, Message
# from functools import wraps
# import requests
# import json
# from flask_session import Session
from flask_pymongo import PyMongo
import urllib.parse
from flask_cors import CORS, cross_origin

password = urllib.parse.quote_plus("qwerty@123")
CONNECTION_STRING = "mongodb+srv://qwerty:{}@be-project.llqsi.mongodb.net/BE-Project?retryWrites=true&w=majority".format(password)


# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('BE-Project')


app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True)
app.config.from_pyfile('config.cfg')
app.config["MONGO_URI"] = CONNECTION_STRING
app.config["CORS_HEADERS"] = "Content-Type"

cors = CORS(app)
mongo = PyMongo(app)

# def execute_db(query,args=()):
#     try:
#         cur=mysql.connection.cursor()
#         cur.execute(query,args)
#         mysql.connection.commit()
#     except:
#         mysql.connection.rollback()
#     finally:
#         cur.close()

# def query_db(query,args=(),one=False):
#     cur=mysql.connection.cursor()
#     result=cur.execute(query,args)
#     if result>0:
#         values=cur.fetchall()
#         return values
#     cur.close()

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect(url_for("auth.login", next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("admin")==False:
#             return redirect(url_for("main.displayLessons", next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function

## Configuring Flask-Mail
# app.config.update(
# 	DEBUG=True,
# 	#EMAIL SETTINGS
# 	MAIL_SERVER='smtp.gmail.com',
# 	MAIL_PORT=465,
# 	MAIL_USE_SSL=True,
# 	MAIL_USERNAME = '#',
# 	MAIL_PASSWORD = '#'
# 	)
# mail = Mail(app)

# def send_mail(title,sender,recipients,message_html):
#     msg = Message(title,
#         sender=sender,
#         recipients=recipients)
#     msg.html = message_html
#     mail.send(msg)
#     return ("Mail Sent")

# Importing Blueprints
# from app.views.main import main
# from app.views.auth import auth
from app.views.api import api

# Registering Blueprints

# app.register_blueprint(main)
# app.register_blueprint(auth)
app.register_blueprint(api)