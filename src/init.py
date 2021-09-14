from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, template_folder='./templates')
directory=os.path.normpath(os.getcwd() + os.sep + os.pardir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directory,'database', 'data.db')