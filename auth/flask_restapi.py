# from flask import Flask
# from flask_restplus import Api
# app = Flask(__name__)
# api = Api(app, version='1.0', title='Healthcare Appointment Scheduling System API', description='API for managing appointments and availability')

# from flask_restplus import fields

# appointment_model = api.model('Appointment', {
#     'id': fields.Integer(required=True, description='The appointment ID'),
#     'date': fields.DateTime(required=True, description='The appointment date and time'),
#     'patient_name': fields.String(required=True, description='The name of the patient'),
#     'doctor_name': fields.String(required=True, description='The name of the doctor'),
# })


from flask import Flask, request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

# Initialize Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)
