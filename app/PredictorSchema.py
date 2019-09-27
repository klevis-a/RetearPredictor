from marshmallow import Schema, fields, validate, post_load
from app.Prediction import Prediction


class PredictorSchemaErrors:
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
    FATTY_INFILTRATION_INVALID_ERROR = 'Please select a Goutallier fatty infiltration classification between 0 and 4 ' \
                                       '(inclusive). '


class PredictorSchema(Schema):
    age = fields.Float(validate=validate.Range(min=19.0, max=90.0), required=True,
                       error_messages=dict([('required', PredictorSchemaErrors.AGE_REQUIRED_ERROR),
                                            ('invalid', PredictorSchemaErrors.AGE_INVALID_ERROR)]))

    gender = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                            error_messages=dict([('required', PredictorSchemaErrors.GENDER_REQUIRED_ERROR),
                                                 ('invalid', PredictorSchemaErrors.GENDER_INVALID_ERROR)]))

    osteoporosis = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                  error_messages=dict(
                                      [('required', PredictorSchemaErrors.OSTEOPOROSIS_REQUIRED_ERROR),
                                       ('invalid', PredictorSchemaErrors.OSTEOPOROSIS_INVALID_ERROR)]))

    work_activity_level = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                         error_messages=dict(
                                             [('required', PredictorSchemaErrors.WORK_ACTIVITY_REQUIRED_ERROR),
                                              ('invalid', PredictorSchemaErrors.WORK_ACTIVITY_INVALID_ERROR)]))

    tear_width = fields.Float(validate=validate.Range(min=0.0, max=60.0), required=True,
                              error_messages=dict([('required', PredictorSchemaErrors.TEAR_WIDTH_REQUIRED_ERROR),
                                                   ('invalid', PredictorSchemaErrors.TEAR_WIDTH_INVALID_ERROR)]))

    tear_retraction = fields.Float(validate=validate.Range(min=0.0, max=60.0), required=True,
                                   error_messages=dict(
                                       [('required', PredictorSchemaErrors.TEAR_RETRACTION_REQUIRED_ERROR),
                                        ('invalid', PredictorSchemaErrors.TEAR_RETRACTION_INVALID_ERROR)]))

    full_thickness = fields.Integer(validate=validate.OneOf((0, 1)), required=True,
                                    error_messages=dict(
                                        [('required', PredictorSchemaErrors.FULL_THICKNESS_REQUIRED_ERROR),
                                         ('invalid', PredictorSchemaErrors.FULL_THICKNESS_INVALID_ERROR)]))

    fatty_infiltration = fields.Integer(validate=validate.OneOf((0, 1, 2, 3, 4)), required=True,
                                        error_messages=dict(
                                            [('required', PredictorSchemaErrors.FATTY_INFILTRATION_REQUIRED_ERROR),
                                             ('invalid', PredictorSchemaErrors.FATTY_INFILTRATION_INVALID_ERROR)]))

    @post_load
    def make_predictor(self, data, **kwargs):
        return Prediction(**data)
