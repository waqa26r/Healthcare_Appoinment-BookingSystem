import MySQLdb
from flask_mysqldb import MySQL
from flask import Blueprint, jsonify, render_template, redirect, url_for, session
from auth import patient_required

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/book-appointments', methods=["POST"])
@patient_required
def book_appointments():
    # Get the user ID from the session
    from __init__ import mysql
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return jsonify({'error': "Session has expired"}),  401
    try:
        
        # Fetch patient details for the logged-in user
        patient_details = get_patient_details(user_id)
        print(patient_details)
        doctor_details = get_doctor_details()
        print(doctor_details)
        return jsonify(patient_details,doctor_details),  200

    
    except Exception as e:
        print(f"An error occurred while fetching user details: {e}")
        return render_template('error.html', message="An error occurred while fetching user details.")

# Function to fetch doctor details from the database
def get_doctor_details():
    try:
        # Execute query to fetch doctor details
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Doc_Name, Speciality FROM doctor_availability")
        doctors = cursor.fetchall()
        return doctors
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()

def get_patient_details(user_id):
    # Connect to the database
    try:
        # Execute query to fetch patient details for the logged-in user
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Name, Email_ID, Gender, Address, Phone_No FROM users WHERE role_id = 3 AND user_id = %s", (user_id,))
        patient = cursor.fetchone()
        return patient
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
     