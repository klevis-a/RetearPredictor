from http import HTTPStatus
from flask import request, abort, jsonify, render_template
from app import app
from app import db
from marshmallow import ValidationError
from app.PredictorSchema import PredictorSchema
from app.Prediction import Prediction

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
    return render_template('viewpredictions.html', predictions=predictions)


@app.route('/')
def index():
    return render_template('index.html')
