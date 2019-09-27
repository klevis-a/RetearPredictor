from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + \
                                        '@' + os.environ['DB_HOST'] + ':' + os.environ['DB_PORT'] + \
                                        '/' + os.environ['DB_NAME']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
