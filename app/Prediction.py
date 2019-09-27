import math
import datetime
from app import db


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Float)
    gender = db.Column(db.Boolean)
    osteoporosis = db.Column(db.Boolean)
    work_activity_level = db.Column(db.Boolean)
    tear_width = db.Column(db.Float)
    tear_retraction = db.Column(db.Float)
    full_thickness = db.Column(db.Boolean)
    fatty_infiltration = db.Column(db.Boolean)
    ip_address = db.Column(db.String(length=15))
    date = db.Column(db.DateTime)
    diebold_likelihood = db.Column(db.Float)
    kwon_likelihood = db.Column(db.Float)
    utah_likelihood = db.Column(db.Float)
    keener_likelihood = db.Column(db.Float)
    combined_likelihood = db.Column(db.Float)

    def __init__(self, age, gender, osteoporosis, work_activity_level, tear_width, tear_retraction, full_thickness,
                 fatty_infiltration, ip_address='', date=datetime.datetime.now(), diebold_likelihood=0.0,
                 kwon_likelihood=0.0, utah_likelihood=0.0, keener_likelihood=0.0, combined_likelihood=0.0):
        self.age = age
        self.gender = gender
        self.osteoporosis = osteoporosis
        self.work_activity_level = work_activity_level
        self.tear_width = tear_width
        self.tear_retraction = tear_retraction
        self.full_thickness = full_thickness
        self.fatty_infiltration = fatty_infiltration
        self.ip_address = ip_address
        self.date = date
        self.diebold_likelihood = diebold_likelihood
        self.kwon_likelihood = kwon_likelihood
        self.utah_likelihood = utah_likelihood
        self.keener_likelihood = keener_likelihood
        self.combined_likelihood = combined_likelihood
        self._predict_retear_rate()

    def append_stamp(self, ip_address):
        self.ip_address = ip_address
        self.date = datetime.datetime.now()

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
