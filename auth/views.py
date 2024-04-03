from flask import Flask, Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash
import bcrypt
import re
import json
from pydantic import BaseModel, ValidationError, validator
from functools import wraps
# from flask_session import Session
from flask_jwt_extended import create_access_token
from flasgger import swag_from



# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)

auth_bp = Blueprint('auth', __name__)
# def patient_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user_id' not in session:
#             return jsonify({'error': "Session has expired"}),  401#  redirect(url_for('auth_bp.login')) 
#         return f(*args, **kwargs)
#     return decorated_function


class UserModel(BaseModel):
    name: str
    email: str
    # age: int
    pwd: str
    # addr: str
    ph_no: int
    
    @validator('email')
    def email_must_contain_domain(cls, v):
        pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}$')
        if '@' not in v:
            raise ValueError('Email must contain @')
        return v
    
    # @validator('age')
    # def age_must_be_positive(cls, v):
    #     if v <= 0:
    #         raise ValueError('Age must be positive')
    #     return v
    
    @validator('name')
    def name_should_be_alpha(cls, v):
        pattern = re.compile(r'^[a-zA-Z ]+$')
        if not pattern.match(v):
            raise ValueError('Name must contain only alphabets and spaces')
        return v
    
    # @validator('addr')
    # def address_must_be_valid(cls, v):
    #     pattern = re.compile(r'^[\w\s]+$')
    #     forbidden_chars = r'\=|\?|@|#|\*'
    #     if not pattern.match(v) or re.search(forbidden_chars, v):
    #         raise ValueError('Address must contain only alphanumeric characters, spaces, and must not include special characters like =, ?, @, #, *')
    #     return v
    
    @validator('pwd')
    def password_must_meet_requirements(cls, v):
        pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*\W).{8,}$')
        if not pattern.match(v):
            raise ValueError('Password must be at least 8 characters long, contain at least one digit, one alphabet character, and one special character')
        return v
    
    @validator('ph_no')
    def phone_number_digits(cls, v):
        pattern = re.compile(r'^\d+$')
        if not pattern.match(str(v)):
            raise ValueError('Phone number should be digits')
        return v
    
register_api_spec = {
    "description": "Register a new user",
    "parameters": [
        {
            "name": "user",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "User name"
                    },
                    "email": {
                        "type": "string",
                        "description": "User email"
                    },
                    "pwd": {
                        "type": "string",
                        "description": "User password"
                    },
                    "ph_no": {
                        "type": "integer",
                        "description": "User phone number"
                    },
                    "role": {
                        "type": "string",
                        "description": "User role"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "User registered successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "Registration successful"
                    }
                }
            }
        },
        "400": {
            "description": "Bad request",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "An error occurred while processing your request"
                    }
                }
            }
        }
    }
}


@auth_bp.route("/register", methods=["POST"])
@swag_from(register_api_spec)
def registration():
    print("hello")
    try:
        from __init__ import mysql
        user_data = request.get_json()
        validation_data = {key: user_data[key] for key in UserModel.model_fields.keys()}
        validated_data = UserModel(**validation_data)


        name = validated_data.name
        email = validated_data.email
        pwd = validated_data.pwd.encode('utf-8')
        ph_no = validated_data.ph_no
        role = user_data.get('role')


        # Handle role-specific fields
        if role == '3':
            age = user_data.get('age')
            addr = user_data.get('addr')
            gender = user_data.get('gender')
            bld_grp = user_data.get('bloodGroup')
        else:
            age = None
            addr = None
            gender = None
            bld_grp = None


        # Perform database operations
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE Email_ID = %s", (email,))
        existing_user = cursor.fetchone()


        if existing_user:
            return jsonify({'error': "Email already exists in the database"}), 400


        salt = bcrypt.gensalt()
        hash_pwd = bcrypt.hashpw(pwd, salt)


        db_users_insert = "INSERT INTO Users (Role_ID, Name, Email_ID, Age, Address, Phone_No, Password, Gender, Blood_Group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        db_users_insert_values = (role, name, email, age, addr, ph_no, hash_pwd, gender, bld_grp)
        cursor.execute(db_users_insert, db_users_insert_values)
        mysql.connection.commit()
        cursor.close()


        return jsonify({'message': "Registration successful"}), 200


    except ValidationError as e:
        error_messages = [error["msg"] for error in e.errors()]
        return jsonify({'errors': error_messages}), 400


    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': "An error occurred while processing your request"}), 500
    

login_api_spec = {
    "description": "Login a user",
    "parameters": [
        {
            "name": "user",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email"
                    },
                    "pwd": {
                        "type": "string",
                        "description": "User password"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Login successful",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string",
                        "description": "JWT access token"
                    },
                    "user_info": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "User ID"
                            },
                            "name": {
                                "type": "string",
                                "description": "User name"
                            },
                            "email_id": {
                                "type": "string",
                                "description": "User email"
                            },
                            "role_id": {
                                "type": "string",
                                "description": "User role ID"
                            },
                            "phone_no": {
                                "type": "string",
                                "description": "User phone number"
                            }
                        }
                    },
                    "message": {
                        "type": "string",
                        "description": "Login message"
                    }
                }
            }
        },
        "400": {
            "description": "Bad request",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        },
        "401": {
            "description": "Unauthorized",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        },
        "500": {
            "description": "Internal server error",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message"
                    }
                }
            }
        }
    }
}

@auth_bp.route("/login", methods=["POST"])
@swag_from(login_api_spec)
def login():
    print("hello")
    from __init__ import mysql
    try:
        cursor = mysql.connection.cursor()
        data = request.get_json()
        print("data recieved")
        email = data.get("email")
        password = data.get("pwd")
        print(email,password)
        
        if not email or not password:
            return jsonify({"message": "Email and password are required."}),  400
        
        cursor.execute("SELECT * FROM users WHERE Email_ID = %s", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"message": "User not found."}),  404
        
        # Create a dictionary from the tuple using column names
        user_dict = {desc[0]: value for desc, value in zip(cursor.description, user)}
        
        provided_password = password.encode('utf-8')
        stored_hashed_password = user_dict['Password'].encode('utf-8')
        flag = bcrypt.checkpw(provided_password, stored_hashed_password)
        
        if not flag:
            return jsonify({"message": "Invalid password."}),  401
        
        # if flag:
        #     # Set the session data
        #     session['user_id'] = user_dict['User_Id']
        #     session['name'] = user_dict['Name']
        #     session['email_id'] = user_dict['Email_ID']
        #     session['role_id'] = user_dict['Role_ID']
        #     session['phone_no'] = user_dict['Phone_No']
        #     print(session)
            
        #     # Create a dictionary from the session data
        #     session_dict = {
        #         'user_id': session['user_id'],
        #         'name': session['name'],
        #         'email_id': session['email_id'],
        #         'role_id': session['role_id'],
        #         'phone_no': session['phone_no']
        #     }
        #     print(session_dict)       
        #     session_json = json.dumps(session_dict)
        #     return jsonify({"session": session_json, "message": "Login successful"}),   200
        # else:
        #     return jsonify({"message": "Invalid user."}),  401

        user_info = {
                'user_id': user_dict['User_ID'],
                'name': user_dict['Name'],
                'email_id': user_dict['Email_ID'],
                'role_id': user_dict['Role_ID'],
                'phone_no': user_dict['Phone_No']
            }
        print(user_info)
    
        if flag:
        # Create a JWT token
            access_token = create_access_token(identity=user_dict['User_ID'])
            print("login successful\n",access_token)
            return jsonify({"access_token": access_token,"user_info": user_info, "message": "Login successful"}),  200
        else:
            return jsonify({"message": "Invalid user."}),  401 
            # create new token for every api

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}),  500

# def is_authenticated():
#     return 'user_id' in session
                                                                                                                                                                                                               