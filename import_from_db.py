import csv
import uuid
import time
from app import field_names
from app.Prediction import PredictionModel, PredictionSchema

with open(r'C:\Users\klevis\Downloads\exportedPredictions_1599937002.csv') as csv_file:
    # skip first line
    next(csv_file, None)
    # id is the first field_name so we skip it
    csv_reader = csv.DictReader(csv_file, fieldnames=list(field_names.keys())[1:], delimiter=',')
    for row in csv_reader:
        predictor_schema = PredictionSchema()
        predictor_data = predictor_schema.load(row)
        prediction_model = PredictionModel(**predictor_data)
        prediction_model.id = str(uuid.uuid4())
        prediction_model.save()
        time.sleep(0.2)
