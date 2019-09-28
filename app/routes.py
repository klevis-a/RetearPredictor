from http import HTTPStatus
from flask import request, abort, jsonify, render_template
import boto3
import os
from marshmallow import ValidationError
import time
from app import app
from app import db
from app import field_names
from app.PredictorSchema import PredictorSchema
from app.Prediction import Prediction
from app import SpreadsheetExport

predictorSchema = PredictorSchema()


@app.errorhandler(HTTPStatus.BAD_REQUEST.value)
def page_not_found(e):
    return jsonify(e.description), HTTPStatus.BAD_REQUEST.value


@app.route('/retearlikelihood', methods=['POST'])
def retear_likelihood():
    try:
        predictor_data = predictorSchema.load(request.form)
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST.value, err.messages)

    predictor_data.append_stamp(request.remote_addr)
    db.session.add(predictor_data)
    db.session.commit()
    return jsonify(
        {'likelihood': predictor_data.combined_likelihood})


@app.route('/viewpredictions')
def view_predictions():
    predictions = Prediction.query.all()
    return render_template('viewpredictions.html', predictions=predictions, names=field_names.keys(), friendly_names=field_names.values())


@app.route('/spreadsheet')
def spreadsheet_export():
    predictions = Prediction.query.all()
    serializer = PredictorSchema(many=True)
    result = serializer.dump(predictions)
    csv_export = SpreadsheetExport.write_csv(result, field_names.keys(), field_names.values())
    file_path = 'csv_exports/' + 'exportedPredictions_' + str(int(time.time())) + '.csv'
    s3 = boto3.resource('s3')
    s3.Bucket(os.environ['S3_EXPORT_BUCKET']).put_object(Key=file_path, Body=csv_export)
    return render_template('spreadsheet.html')


@app.route('/')
def index():
    return render_template('index.html')
