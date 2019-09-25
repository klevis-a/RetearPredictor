import math


class PredictorObject:
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

    def predict_retear_rate(self):
        diebold_likelihood, diebold_sample_size = self._diebold_prediction()
        kwon_likelihood, kwon_sample_size = self._kwon_prediction()
        utah_likelihood, utah_sample_size = self._utah_prediction()
        keener_likelihood, keener_sample_size = self._keener_prediction()
        return (diebold_likelihood * diebold_sample_size + kwon_likelihood * kwon_sample_size +
                utah_likelihood * utah_sample_size + keener_likelihood * keener_sample_size) / \
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
                + (self.age > 70) * 2 + (self.fatty_infiltration >= 2) * 3 + self._kwon_retraction_score()
        return -0.0006 * score ** 3 + 0.0131 * score ** 2 + 0.009 * score, 603

    def _utah_prediction(self):
        score = -3.282 + self.tear_retraction * 0.09
        return math.exp(score) / (1 + math.exp(score)), 110

    def _keener_prediction(self):
        return 1 / (1 + math.exp(5.263 - 0.105 * self.tear_width - self.gender * 2.05)), 115
