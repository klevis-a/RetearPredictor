from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_port = os.environ['DB_PORT']
db_name = os.environ['DB_NAME']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + ':' + db_port \
                                        + '/' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes
