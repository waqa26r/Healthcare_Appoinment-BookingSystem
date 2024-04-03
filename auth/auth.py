# app/auth/views.py
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import bcrypt

auth_bp = Blueprint('auth', __name__)

# Custom decorator to check if user is authenticated and has the patient role
def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': "Session has expired"}),  401#  redirect(url_for('auth_bp.login')) 
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/register", methods=["POST"])
def registration():
    from __init__ import mysql
    try:
        cursor = mysql.connection.cursor()
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("pwd")
        gender = data.get("gender")
        addr = data.get("addr")
        phone_no = data.get("phone_no")
        role = data.get("role") #role = admin doctor patient
        blood_grp = data.get("blood_grp")

        if role == "patient":
            role_value = 3
        elif role == "doctor":
            role_value = 2
        elif role == "admin":
            role_value = 1

        

        password = password.encode('utf-8')  # Convert to bytes
        salt = bcrypt.gensalt()  # Generate a salt
        hashed_password = bcrypt.hashpw(password, salt)  # Hash the password with the salt
        hash_pwd=hashed_password.decode('utf-8')  # Return the hashed password as a string
 

        db_users_insert = "INSERT INTO Users (Name, Email_ID, Password, Gender, Address, Phone_No, Role_ID, Blood_Group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        db_users_insert_values = (name, email, hash_pwd, gender, addr, phone_no, role_value,blood_grp)

        # Executing SQL Statements
        cursor.execute(db_users_insert, db_users_insert_values)
        # Saving the actions performed on the DB
        mysql.connection.commit()

        
        # Closing the cursor
        cursor.close()

        # cursor.execute("SELECT * FROM Users WHERE Email_ID = %s", (email,))
        # doctor_details = cursor.fetchone()
        # column_names = [desc[0] for desc in cursor.description]
        # doctor_data = dict(zip(column_names, doctor_details))

        # db_doctors_insert="INSERT INTO doctors(Doc_ID, Doc_Name) SELECT User_Id, Name FROM users WHERE Role_ID = 2 "
        # print(doctor_data['User_Id'],doctor_data['Name'])
        #     # db_doctors_insert_values = (doctor_data['User_Id'],doctor_data['Name'])
        # cursor.execute(db_doctors_insert)
        # mysql.connection.commit()
        
        return jsonify({'message': "User data saved successfully"}),  201

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}),  500


#for login
@auth_bp.route("/login", methods=["POST"])
def login():
    from __init__ import mysql
    try:
        cursor = mysql.connection.cursor()
        data = request.get_json()
        email = data.get("email")
        password = data.get("pwd")
        role = data.get("role")
       
        if role == "patient":
            role_value = 3
        elif role == "doctor":
            role_value = 2
        elif role == "admin":
            role_value = 1
        
        if not email or not password:
            return jsonify({"message": "Email and password are required."}),   400

        cursor.execute("SELECT * FROM Users WHERE Email_ID = %s", (email,))
      
        user = cursor.fetchone()

       

        if not user:
            return jsonify({"message": "User not found."}),   404
        if not role:
            return jsonify({"message": "Please select a role."}),   404
        
        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]
 
        # Construct a dictionary mapping column names to values
        user_data = dict(zip(column_names, user))
        print(user_data['Password'])
        
        provided_password = password.encode('utf-8')
        stored_hashed_password = user_data['Password'].encode('utf-8')
        flag = bcrypt.checkpw(provided_password, stored_hashed_password)

        if not flag:
            return jsonify({"message": "Invalid password."}),   401
        
        session['user_id'] = user_data['User_Id']
        print(session)
        
        if flag and user_data['Role_ID']== 1 and role_value == 1:
            return jsonify({"message": "Login successful as Admin."}),   200
        elif flag and user_data['Role_ID']== 2 and role_value == 2:

            # cursor.execute("SELECT * FROM Users WHERE Email_ID = %s", (email,))
            # doctor_details = cursor.fetchone()
            # column_names = [desc[0] for desc in cursor.description]
            # doctor_data = dict(zip(column_names, doctor_details))

            # db_doctors_insert="INSERT INTO doctors(Doc_ID, Doc_Name) SELECT User_Id, Name FROM users WHERE Role_ID = 2 "
            # print(doctor_data['User_Id'],doctor_data['Name'])
            # # db_doctors_insert_values = (doctor_data['User_Id'],doctor_data['Name'])
            # cursor.execute(db_doctors_insert)
            # mysql.connection.commit()
            return jsonify({"message": "Login successful as Doctor."}),   200
           
        elif flag and user_data['Role_ID']== 3 and role_value == 3: 
            if is_authenticated():
                return jsonify({"message": "Login successful as Patient."}),   200
            #     return redirect(url_for('home')), 
            
        else:
            return jsonify({"message": "Invalid user."}),   401

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}),   500

def is_authenticated():
    return 'user_id' in session
