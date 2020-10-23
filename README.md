#### Live Code Demos

* [Calculate retear prediction likelihood](https://tinyurl.com/cufftear)
* [Google Map of recorded predictions](https://tinyurl.com/cufftear/map)

#### Technical Details

The current incarnation of the web application utilizes [Lambda](https://aws.amazon.com/lambda/) and [DynamoDB](https://aws.amazon.com/dynamodb/) from [Amazon Web Services](https://aws.amazon.com/). These technologies (along with [Zappa](https://github.com/Miserlou/Zappa)) make it simple to update, test, and deploy the application. Under the covers the web application utilizes:

* [Flask](https://github.com/pallets/flask) as the application framework
* [PynamoDB](https://github.com/pynamodb/PynamoDB) as the Object Relational Mapper for DynamoDB
* [Marshmallow](https://github.com/marshmallow-code/marshmallow) as the Object Relational Mapper for JavaScript Object Notation (JSON)

Finally, thanks to Python's fantastic open-source community ([Flask-GoogleMaps](https://github.com/flask-extensions/Flask-GoogleMaps)), the web application plots each retear prediction on a Google map.

#### Background

Rotator cuff tears remain a therapeutic challenge for orthopedic surgeons. Among other concerns, the fundamental question of whether a rotator cuff repair should be repaired or not still remains unanswered. Various criteria enter into the decision-making process such as the patient's age, gender, activity level, tear severity, outlook on surgery, etc. Through retrospective analysis (typically multivariate logistic regression), prior investigations have determined correlations between the aforementioned criteria and repair integrity. The surgeons in our group have combined the results from several studies, and their own datasets, to create an algorithm for predicting rotator cuff retear likelihood rate based on patient/tear characteristics.

To make this algorithm easily accessible, I created a simple web application that can be accessed on a mobile phone. In addition to providing a prediction, our group was interested in recording the patient/tear characteristics input into the application for future analysis; therefore, a backend database was necessary. Since input data is being stored in the database, I thought it would be fun to also create a Google map of prediction location (based on IP address).