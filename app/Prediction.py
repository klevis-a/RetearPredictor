import os
import math
import datetime
import uuid
from marshmallow import Schema, fields, validate
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute, UTCDateTimeAttribute


class PredictionSchema(Schema):
    """Validator for web service input, relying on Marshmallow."""

    AGE_REQUIRED_ERROR = 'Please enter age of patient.'
    AGE_INVALID_ERROR = 'Age of patient must be between 19 and 90.'

    GENDER_REQUIRED_ERROR = 'Please select gender of patient.'
    GENDER_INVALID_ERROR = 'Please select male or female for gender of patient.'

    OSTEOPOROSIS_REQUIRED_ERROR = 'Please select whether the patient has osteroporosis or not.'
    OSTEOPOROSIS_INVALID_ERROR = 'Please select Yes or No in the Osteroporosis field.'

    WORK_ACTIVITY_REQUIRED_ERROR = 'Please select the work activity level for the patient.'
    WORK_ACTIVITY_INVALID_ERROR = 'Please select Yes or No in the High Level of Work Activity field.'

    TEAR_WIDTH_REQUIRED_ERROR = 'Please enter a tear width.'
    TEAR_WIDTH_INVALID_ERROR = 'Tear width must be between 0 and 60 mm.'

    TEAR_RETRACTION_REQUIRED_ERROR = 'Please enter a tear retraction.'
    TEAR_RETRACTION_INVALID_ERROR = 'Tear retraction must be between 0 and 60 mm.'

    FULL_THICKNESS_REQUIRED_ERROR = 'Please select whether this is a full thickness tear or not.'
    FULL_THICKNESS_INVALID_ERROR = 'Please select Yes or No in the Full Thickness Tear field.'

    FATTY_INFILTRATION_REQUIRED_ERROR = 'Please select a Goutallier fatty infiltration classification.'
    FATTY_INFILTRATION_INVALID_ERROR = 'Please select a Goutallier fatty infiltration classification <2 or >=2.'

    age = fields.Float(validate=validate.Range(min=19.0, max=90.0), required=True,
                       error_messages=dict([('required', AGE_REQUIRED_ERROR),
                                            ('invalid', AGE_INVALID_ERROR)]))

    gender = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                            error_messages=dict([('required', GENDER_REQUIRED_ERROR),
                                                 ('invalid', GENDER_INVALID_ERROR)]))

    osteoporosis = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                  error_messages=dict(
                                      [('required', OSTEOPOROSIS_REQUIRED_ERROR),
                                       ('invalid', OSTEOPOROSIS_INVALID_ERROR)]))

    work_activity_level = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                         error_messages=dict(
                                             [('required', WORK_ACTIVITY_REQUIRED_ERROR),
                                              ('invalid', WORK_ACTIVITY_INVALID_ERROR)]))

    tear_width = fields.Float(validate=validate.Range(min=0.0, max=60.0), required=True,
                              error_messages=dict([('required', TEAR_WIDTH_REQUIRED_ERROR),
                                                   ('invalid', TEAR_WIDTH_INVALID_ERROR)]))

    tear_retraction = fields.Float(validate=validate.Range(min=0.0, max=60.0), required=True,
                                   error_messages=dict(
                                       [('required', TEAR_RETRACTION_REQUIRED_ERROR),
                                        ('invalid', TEAR_RETRACTION_INVALID_ERROR)]))

    full_thickness = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                    error_messages=dict(
                                        [('required', FULL_THICKNESS_REQUIRED_ERROR),
                                         ('invalid', FULL_THICKNESS_INVALID_ERROR)]))

    fatty_infiltration = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                        error_messages=dict(
                                            [('required', FATTY_INFILTRATION_REQUIRED_ERROR),
                                             ('invalid', FATTY_INFILTRATION_INVALID_ERROR)]))

    id = fields.String()
    ip_address = fields.String()
    date = fields.DateTime()
    diebold_likelihood = fields.Float()
    kwon_likelihood = fields.Float()
    utah_likelihood = fields.Float()
    keener_likelihood = fields.Float()
    combined_likelihood = fields.Float()


class PredictionModel(Model):
    """DynamoDB table model relying on pynamodb."""

    class Meta:
        table_name = os.environ['DYNAMO_TABLE_NAME']
        region = os.environ['DYNAMO_REGION']
        write_capacity_units = os.environ['DYNAMO_WCU']
        read_capacity_units = os.environ['DYNAMO_RCU']

    id = UnicodeAttribute()
    age = NumberAttribute()
    gender = BooleanAttribute()
    osteoporosis = BooleanAttribute()
    work_activity_level = BooleanAttribute()
    tear_width = NumberAttribute()
    tear_retraction = NumberAttribute()
    full_thickness = BooleanAttribute()
    fatty_infiltration = BooleanAttribute()
    ip_address = UnicodeAttribute()
    date = UTCDateTimeAttribute()
    diebold_likelihood = NumberAttribute()
    kwon_likelihood = NumberAttribute()
    utah_likelihood = NumberAttribute()
    keener_likelihood = NumberAttribute()
    combined_likelihood = NumberAttribute()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mint(self, ip_address):
        self.id = str(uuid.uuid4())
        self.ip_address = ip_address
        self.date = datetime.datetime.now()


class Prediction:
    """Prediction based on supplied input."""

    # The values for the fields below can be found in index.html but I am listing them here for ease of use:
    # gender: Female (True, 1), Male (False, 0)
    # osteoporosis: Yes (True, 1), No (False, 0)
    # work_activity_level: High (1), Not High (0)
    # full_thickness: Yes (True, 1), No (False, 0)
    # fatty infiltration: Goutallier Classification >= 2 (True, 1), Goutallier Classification <>=> 2 (False, 0)

    def __init__(self, age, gender, osteoporosis, work_activity_level, tear_width, tear_retraction, full_thickness,
                 fatty_infiltration):
        self.age = age
        self.gender = gender
        self.osteoporosis = osteoporosis
        self.work_activity_level = work_activity_level
        self.tear_width = tear_width
        self.tear_retraction = tear_retraction
        self.full_thickness = full_thickness
        self.fatty_infiltration = fatty_infiltration
        self._predict_retear_rate()

    def _predict_retear_rate(self):
        self.diebold_likelihood, diebold_sample_size = self._diebold_prediction()
        self.kwon_likelihood, kwon_sample_size = self._kwon_prediction()
        self.utah_likelihood, utah_sample_size = self._utah_prediction()
        self.keener_likelihood, keener_sample_size = self._keener_prediction()
        self.combined_likelihood = (self.diebold_likelihood * diebold_sample_size +
                                    self.kwon_likelihood * kwon_sample_size + self.utah_likelihood * utah_sample_size +
                                    self.keener_likelihood * keener_sample_size) / \
                                   (diebold_sample_size + kwon_sample_size + utah_sample_size + keener_sample_size)

    def _tear_area(self):
        return self.tear_width * self.tear_retraction

    def _kwon_retraction_score(self):
        if self.tear_retraction < 10:
            return 0
        if self.tear_retraction < 20:
            return 1
        if self.tear_retraction < 30:
            return 2
        return 4

    def _diebold_prediction(self):
        score = -5.833 + self.age * 0.0451 - self.gender * 0.511 + self._tear_area() * 0.00094 \
                + self.full_thickness * 1.182
        return math.exp(score) / (1 + math.exp(score)), 1600

    def _kwon_prediction(self):
        score = self.work_activity_level * 2 + self.osteoporosis * 2 + (self.tear_width > 25) * 2 \
                + (self.age > 70) * 2 + self.fatty_infiltration * 3 + self._kwon_retraction_score()
        return -0.0006 * score ** 3 + 0.0131 * score ** 2 + 0.009 * score, 603

    def _utah_prediction(self):
        score = -3.282 + self.tear_retraction * 0.09
        return math.exp(score) / (1 + math.exp(score)), 110

    def _keener_prediction(self):
        return 1 / (1 + math.exp(5.263 - 0.105 * self.tear_width - self.gender * 2.05)), 115
