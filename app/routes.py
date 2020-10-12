from http import HTTPStatus
from flask import request, abort, jsonify, render_template, redirect
import boto3
import os
from marshmallow import ValidationError
import time
import geoip2.database
from flask_googlemaps import Map
from app import app, field_names, SpreadsheetExport
from app.Prediction import Prediction, PredictionModel, PredictionSchema


@app.errorhandler(HTTPStatus.BAD_REQUEST.value)
def page_not_found(e):
    return jsonify(e.description), HTTPStatus.BAD_REQUEST.value


@app.route('/retearlikelihood', methods=['POST'])
def retear_likelihood():
    # validate the input
    predictor_data = None
    try:
        predictor_schema = PredictionSchema()
        predictor_data = predictor_schema.load(request.form)
    except ValidationError as err:
        abort(HTTPStatus.BAD_REQUEST.value, err.messages)

    # create a prediction
    prediction = Prediction(**predictor_data)

    # save it to the database
    prediction_model = PredictionModel(**vars(prediction))
    # the user supplied data doesn't have a unique ID, an IP address, or a timestamp - that is what mint does
    prediction_model.mint(request.remote_addr)
    prediction_model.save()
    return jsonify(
        {'likelihood': prediction_model.combined_likelihood})


@app.route('/viewpredictions')
def view_predictions():
    # read the database and create a summary page
    predictions = PredictionModel.scan()
    return render_template('viewpredictions.html', predictions=predictions, names=field_names.keys(),
                           friendly_names=field_names.values())


@app.route('/spreadsheet')
def spreadsheet_export():
    # this is just a simple way to get a json representation of the database
    # the json representation returns a list of dictionaries - which is then very easy to write to CSV
    predictions = PredictionModel.scan()
    serializer = PredictionSchema(many=True)
    result = serializer.dump(predictions)
    csv_export = SpreadsheetExport.write_csv(result, field_names.keys(), field_names.values())
    # store the generated CSV file to the specified S3 bucket
    file_path = 'csv_exports/' + 'exportedPredictions_' + str(int(time.time())) + '.csv'
    s3_resource = boto3.resource('s3')
    s3_resource.Bucket(os.environ['S3_BUCKET']).put_object(Key=file_path, Body=csv_export)
    s3_client = boto3.client('s3')
    # generate a URL for the file that expires in 5 minutes
    export_url = s3_client.generate_presigned_url('get_object',
                                                  Params={'Bucket': os.environ['S3_BUCKET'], 'Key': file_path},
                                                  ExpiresIn=300)
    return redirect(export_url, 302)


@app.route('/map')
def create_map():
    if 'MMDB_PATH_LOCAL' in os.environ:
        reader = geoip2.database.Reader(os.environ['MMDB_PATH_LOCAL'])
    else:
        # this app is designed to run as on AWS lambda, where local storage is not persistent
        # so first we check whether the temporary directory for the lambda app already has the geo IP database
        # if not, then download it from S3
        s3_path_split = os.environ['MMDB_PATH_S3'].split('/')
        mmdb_file_name = s3_path_split[-1]
        mmdb_file_fullpath = os.path.join(os.environ['TMP_DIR'], mmdb_file_name)
        if not os.path.exists(mmdb_file_fullpath):
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(os.environ['S3_BUCKET'])
            bucket.download_file(os.environ['MMDB_PATH_S3'], mmdb_file_fullpath)
        reader = geoip2.database.Reader(mmdb_file_fullpath)

    predictions = PredictionModel.scan()
    markers = []
    for prediction in predictions:
        if prediction.combined_likelihood < 0.3:
            marker_icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
        elif prediction.combined_likelihood < 0.7:
            marker_icon = 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
        else:
            marker_icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        reader_response = reader.city(prediction.ip_address)
        infobox = '<div class="gmaps_class">' + str(int(prediction.combined_likelihood * 100)) + '%</div'
        markers.append({
            'icon': marker_icon,
            'lat': reader_response.location.latitude,
            'lng': reader_response.location.longitude,
            'infobox': infobox
        })

    predictions_map = Map(
        identifier='predictions_map',
        lat=40.7649368,
        lng=-111.8421021,
        markers=markers,
        fit_markers_to_bounds=True,
        style='height:800px;width:800px;margin:0;'
    )

    return render_template('map.html', predictions_map=predictions_map)


@app.route('/')
def index():
    return render_template('index.html')
