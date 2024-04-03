from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from views import auth_bp
from fill_availabilty import fill_availability_bp
from appointments import appointments_bp
from appointment_booking import appointment_booking_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from datetime import timedelta
# from flask_restplus import Api, Resource
# from auth import auth_bp

 
load_dotenv()
 
app = Flask(__name__)
CORS(app)
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
 
# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('HOST')
app.config['MYSQL_PORT'] = int(os.getenv('DATABASE_PORT'))  # Default MySQL port
app.config['MYSQL_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DATABASE_NAME')
app.secret_key=os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY']= 'Parkar@123'
 
mysql = MySQL(app)
jwt= JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=45)
 
 
app.register_blueprint(auth_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(fill_availability_bp)
app.register_blueprint(appointment_booking_bp)

@app.route("/")
def home():
    return "Welcome to the Healthcare Appointment Scheduling System!"


check_db_api_spec = {
    "description": "Check database connection",
    "responses": {
        "200": {
            "description": "Database connection successful",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Success message"
                    },
                    "database": {
                        "type": "string",
                        "description": "Name of the connected database"
                    }
                }
            }
        },
        "500": {
            "description": "Failed to connect to the database",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Error message"
                    },
                    "error": {
                        "type": "string",
                        "description": "Detailed error information"
                    }
                }
            }
        }
    }
}

@app.route("/check_db")
@swag_from(check_db_api_spec)
def check_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        cursor.close()
        return jsonify({"message": "Database connection successful.", "database": result[0]})
    except Exception as e:
        return jsonify({"message": "Failed to connect to the database.", "error": str(e)}),  500
 
if __name__ == "__main__":
    app.run(debug=True)