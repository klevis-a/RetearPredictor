from flask import Flask
import os
from flask_googlemaps import GoogleMaps
from app.Prediction import PredictionModel

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = os.environ['GOOGLEMAPS_KEY']
GoogleMaps(app)

field_names = {
    'id': 'UUID',
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

# this allows local testing
if 'DYNAMO_HOST' in os.environ:
    PredictionModel.Meta.host = os.environ['DYNAMO_HOST']
