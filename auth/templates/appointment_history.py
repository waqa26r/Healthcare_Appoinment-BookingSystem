import datetime
from flask import Blueprint, jsonify, session,  request  
from flask_jwt_extended import jwt_required
 
appointment_history_bp = Blueprint('appointment_history', __name__)
 
@appointment_history_bp.route('/appointment_history_details', methods=["POST"])
@jwt_required()
def get_appointment_history():
    try:
        from __init__ import mysql
        
        # Get patient ID and name from session
        print("Hello")
        
        data = request.get_json()
        print(data)
        parsed_data = data.get('parsedData')

# Now, you can access 'name' and 'user_id' from the nested dictionary
        patient_name = parsed_data.get('name')
        patient_id = parsed_data.get('user_id')
        # Extract the user ID from the parsed data
        # patient_id = data.get('user_id')
        print(patient_id)
        # patient_name = data.get('name')
        print(patient_name)
        # Connect to the database
        cursor = mysql.connection.cursor()
        
        # Query to fetch appointment history
        query = """
            SELECT u.Name AS Doctor_Name, a.appt_date, a.time_slot, a.status
            FROM Appointment a
            JOIN users u ON a.Doc_ID = u.User_ID
            WHERE a.Patient_ID = %s and a.status='pending'
        """
        
        cursor.execute(query, (patient_id,))
        # cursor.execute(query, (1,))
        appointment_history_data = cursor.fetchall()
        
        # Initialize a list to store appointment history
        appointment_history = []
        
        # Iterate over the fetched data and format it
        for appointment in appointment_history_data:
            # Convert the string date to a datetime object
            appointment_date = datetime.datetime.strptime(str(appointment[1]), '%Y-%m-%d')
            
            # Format the date as a string
            formatted_appointment_date = appointment_date.strftime('%Y-%m-%d')
            
            # Create a dictionary for each appointment
            appointment_details = {
                'patient_name': patient_name,
                'doctor_name': appointment[0],
                'appointment_date': formatted_appointment_date,
                'time_slot': appointment[2],
                'status': appointment[3]
            }
            
            # Append the appointment details to the list
            appointment_history.append(appointment_details)
        
        # Close the cursor
        cursor.close()
        
        # Return the appointment history as JSON response
        return jsonify({'appointment_history': appointment_history}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500