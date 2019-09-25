from marshmallow import Schema, fields, validate, post_load
from PredictorObject import PredictorObject


class PredictorSchema(Schema):
    age = fields.Float(validate=validate.Range(min=18.0, max=100.0), required=True,
                       error_messages=dict([('required', 'Please enter age of patient.'),
                                            ('invalid', 'Age of patient must be between 18 and 100.')]))

    gender = fields.Integer(validate=validate.OneOf((1, 2)), required=True,
                            error_messages=dict([('required', 'Please select gender of patient.'),
                                                 ('invalid', 'Please select male or female for gender of patient.')]))

    osteoporosis = fields.Integer(validate=validate.OneOf((1, 2)), required=True,
                                  error_messages=dict(
                                      [('required', 'Please select whether the patient has osteroporosis or not.'),
                                       ('invalid', 'Please select Yes or No in the Osteroporosis field.')]))

    work_activity_level = fields.Integer(validate=validate.OneOf((1, 2)), required=True,
                                         error_messages=dict(
                                             [('required', 'Please select the work activity level for the patient.'),
                                              ('invalid',
                                               'Please select Yes or No in the High Level of Work Activity field.')]))

    tear_width = fields.Float(validate=validate.Range(min=0.0, max=20.0), required=True,
                              error_messages=dict([('required', 'Please enter a tear width.'),
                                                   ('invalid', 'Tear width must be between 0 and 20 mm.')]))

    tear_retraction = fields.Float(validate=validate.Range(min=0.0, max=20.0), required=True,
                                   error_messages=dict([('required', 'Please enter a tear retraction.'),
                                                        ('invalid', 'Tear retraction must be between 0 and 20 mm.')]))

    full_thickness = fields.Integer(validate=validate.OneOf((1, 2)), required=True,
                                    error_messages=dict(
                                        [('required', 'Please select whether this is a full thickness tear or not.'),
                                         ('invalid', 'Please select Yes or No in the Full Thickness Tear field.')]))

    fatty_infiltration = fields.Integer(validate=validate.OneOf((0, 1, 2, 3, 4)), required=True,
                                        error_messages=dict([('required',
                                                              'Please select a Goutallier fatty infiltration '
                                                              'classification.'),
                                                             ('invalid',
                                                              'Please select a Goutallier fatty infiltration '
                                                              'classification between 0 and 4 (inclusive).')]))

    @post_load
    def make_predictor(self, data, **kwargs):
        return PredictorObject(**data)
