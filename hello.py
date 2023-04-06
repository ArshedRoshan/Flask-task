from flask import Flask,redirect,url_for,request,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def apps():
   app = Flask(__name__,template_folder='templates')
   app.config['SECRET_KEY'] = 'your secret key'
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/flask-task1'
   db.init_app(app)
   migrate = Migrate(app, db)
   
   app.debug = True
   return app








   
   
   

   



    