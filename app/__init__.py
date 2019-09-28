from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['DB_USER'] + ':' + os.environ['DB_PASS'] + \
                                        '@' + os.environ['DB_HOST'] + ':' + os.environ['DB_PORT'] + \
                                        '/' + os.environ['DB_NAME']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

field_names = {
    'date': 'Date/Time',
    'ip_address': 'IP Address',
    'age': 'Age',
    'gender': 'Gender',
    'osteoporosis': 'Osteoporosis',
    'work_activity_level': 'High Level Work Activity',
    'tear_width': 'Tear Width (mm)',
    'tear_retraction': 'Tear Retraction (mm)',
    'full_thickness': 'Fully Thickness Tear',
    'fatty_infiltration': 'Goutallier Classification',
    'diebold_likelihood': 'Diebold Likelihood',
    'kwon_likelihood': 'Kwon Likelihood',
    'utah_likelihood': 'Utah Likelihood',
    'keener_likelihood': 'Keener Likelihood',
    'combined_likelihood': 'Combined Likelihood'
}
