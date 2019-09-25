from http import HTTPStatus
from flask import Flask, request, abort, jsonify, render_template
from marshmallow import ValidationError
from PredictorSchema import PredictorSchema

app = Flask(__name__)
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

    return jsonify(
        {'likelihood': predictor_data.predict_retear_rate()})


@app.route('/')
def index():
    return render_template('index.html')


# We only need this for local development.
if __name__ == '__main__':
    app.run()
