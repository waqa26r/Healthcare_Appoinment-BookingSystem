from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
 
appointment_booking_bp = Blueprint('appointment_booking', __name__)

@appointment_booking_bp.route('/doctor_speciality', methods=['GET'])
def get_doctors():
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        query = "SELECT users.Name AS doc_name, doctor_availability.Speciality AS doc_speciality FROM users INNER JOIN doctor_availability ON users.User_ID = doctor_availability.Doc_ID"
        cursor.execute(query)
        doctors = cursor.fetchall()
        cursor.close()
        print("getdoc")
        # Format the data as a list of dictionaries
        doctor_list = [{"id": doc[0], "name": doc[1], "speciality": doc[2]} for doc in doctors]
        
        return jsonify(doctor_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500