from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
 
fill_availability_bp = Blueprint('fill_availability', __name__)

@fill_availability_bp.route('/doctor_profile', methods=['GET', 'POST'])
@jwt_required()
def get_doctor_details():
    try:
        # Retrieve the user's identity from the JWT
        user_id = get_jwt_identity()
        doctor = fetch_doctor_details_by_user_id(user_id)

        return jsonify(doctor),  200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}),  500

def fetch_doctor_details_by_user_id(user_id):
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        query = "SELECT Name, Email_ID, Phone_No FROM users WHERE User_ID = %s"
        cursor.execute(query, (user_id,))
        doctor_details = cursor.fetchone()
        cursor.close()

        if doctor_details:
            doctor = {
                "doctor_name": doctor_details[0],
                "doctor_email": doctor_details[1],
                "doctor_phone": doctor_details[2]
            }
            return doctor
        else:
            return {"error": "Doctor details not found"}

    except Exception as e:
        print(f"Error fetching doctor details: {e}")
        return {"error": str(e)}
    
# send data from doctor_availability and user table in json format to doctor form
@fill_availability_bp.route('/doctor_speciality', methods=['GET'])
@jwt_required()
def get_doctors():
    print("get_doctors()")
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        query = "SELECT DISTINCT users.User_ID AS id, users.Name AS doc_name, doctor_availability.Speciality AS doc_speciality FROM users INNER JOIN doctor_availability ON users.User_ID = doctor_availability.Doc_ID"
        cursor.execute(query)
        doctors = cursor.fetchall()
        cursor.close()
        print("getdoc")
        # Format the data as a list of dictionaries
        doctor_list = [{"id": doc[0], "name": doc[1], "speciality": doc[2]} for doc in doctors]
        print(doctor_list)
        
        return jsonify(doctor_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

# get data from doctor form to fill availability in doctor_availabilty table
show_availability_api_spec = {
    "description": "Show doctor availability",
    "parameters": [
        {
            "name": "doctor_id",
            "in": "query",
            "type": "string",
            "required": "true",
            "description": "ID of the doctor"
        }
    ],
    "responses": {
        "200": {
            "description": "Availability data retrieved successfully",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Doctor ID"
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of availability"
                        },
                        "time": {
                            "type": "string",
                            "description": "Time slot of availability"
                        }
                    }
                }
            }
        },
        "404": {
            "description": "No availability data found",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
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

@fill_availability_bp.route('/show_availability', methods=['GET'])
@jwt_required()
@swag_from(show_availability_api_spec)
def doctor_availability():
    print("hello")
    doctor_id = request.args.get('doctor_id')  # Use request.args.get to get the doctor_id from query parameters
    print(f"Received doctor_id: {doctor_id}")
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT Doc_ID, Date_Available, start_time, end_time  FROM doctor_availability WHERE Doc_ID = %s", (doctor_id,))
        availability_data = cursor.fetchall()
        cursor.close()

        # Check if availability_data is empty
        if not availability_data:
            print("No availability data found for the given doctor_id.")
            return jsonify({"error": "No availability data found"}),  404

        availability = [{'id': row[0],'date': row[1], 'start_time': row[2], 'end_time': row[3]} for row in availability_data]
        print(availability)  # Print the availability data

        return jsonify(availability),  200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Print the error message
        return jsonify({"error": str(e)}),  500
    
# appointment history table data fetched from appointment form
appointment_history_api_spec = {
    "description": "Book an appointment",
    "parameters": [
        {
            "name": "appointment",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "doctor_id": {
                        "type": "string",
                        "description": "ID of the doctor"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date of the appointment"
                    },
                    "timeslot": {
                        "type": "string",
                        "description": "Time slot of the appointment"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Appointment booked successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Success message"
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

@fill_availability_bp.route('/appointment_history', methods=['POST'])
@jwt_required()
@swag_from(appointment_history_api_spec)
def appt_history():
    print("appt table")
    try:
        from __init__ import mysql
        # Retrieve the user's identity from the JWT
        patient_id = get_jwt_identity()
        print(patient_id)
        # Assuming the request data is sent as JSON
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        date = data.get('date')
        # timeslot = data.get('timeslot')
        start_time=data.get('start_time')
        end_time=data.get('end_time')
        status = 'pending'  # Assuming status is initially set to 'pending'
        
        # Insert into database
        cursor = mysql.connection.cursor()
        insert_query = "INSERT INTO Appointment(Patient_id, Doc_id, appt_date, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (patient_id, doctor_id, date, start_time, end_time, status))

        delete_query= "DELETE FROM doctor_availability WHERE Doc_ID=%s AND Date_Available= %s AND start_time=%s AND end_time=%s"
        cursor.execute(delete_query, (doctor_id, date, start_time, end_time))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Appointment booked successfully."}),  200
    
    except Exception as e:
        return jsonify({"error": str(e)}),  500
    
def update_status():
    try:
        from __init__ import mysql

        cursor = mysql.connection.cursor()
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        update_query = "UPDATE Appointment SET status= 'completed' WHERE appt_date < %s"
        cursor.execute(update_query, (current_datetime,))

        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        print("Error updating appointment status: ", e)


add_availability_api_spec = {
    "description": "Add doctor availability",
    "parameters": [
        {
            "name": "availability",
            "in": "body",
            "required": "true",
            "schema": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date of availability"
                    },
                    "startTime": {
                        "type": "string",
                        "description": "Start time of availability"
                    },
                    "endTime": {
                        "type": "string",
                        "description": "End time of availability"
                    },
                    "specialty": {
                        "type": "string",
                        "description": "Specialty of the doctor"
                    }
                }
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Availability added successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Success message"
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

@fill_availability_bp.route('/add_availability', methods=['POST'])
@jwt_required()
@swag_from(add_availability_api_spec)
def add_availability():
    print("fill doctor_availability")
    try:
        from __init__ import mysql
        # Retrieve the user's identity from the JWT
        user_id = get_jwt_identity()
        data = request.get_json()

        # Extract data from the request
        doc_id = user_id
        date = data['date']
        start_time = data['startTime']
        end_time = data['endTime']
        specialty = data['specialty']

        # Insert the data into the database
        cursor = mysql.connection.cursor()
        query = "INSERT INTO doctor_availability (Doc_ID, Date_Available, start_time, end_time, Speciality) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (doc_id, date, start_time, end_time, specialty))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Availability added successfully"}),  200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}),  500
    
fetch_dates_api_spec = {
    "description": "Fetch available dates for a specific doctor",
    "parameters": [
        {
            "name": "doctor_id",
            "in": "query",
            "required": "true",
            "type": "string",
            "description": "The ID of the doctor for which to fetch available dates"
        }
    ],
    "responses": {
        "200": {
            "description": "A list of available dates for the specified doctor",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The available date"
                        }
                    }
                }
            }
        },
        "404": {
            "description": "No availability data found for the given doctor_id",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
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
    
@fill_availability_bp.route('/fetch_dates', methods=['GET'])
@jwt_required()
@swag_from(fetch_dates_api_spec)
def fetch_dates():
    print("fetch_dates")
    doctor_id = request.args.get('doctor_id')  # Use request.args.get to get the doctor_id from query parameters
    print(f"Received doctor_id: {doctor_id}")
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT Date_Available FROM doctor_availability WHERE Doc_ID = %s", (doctor_id,))
        date_data = cursor.fetchall()
        cursor.close()

        if not date_data:
            print("No availability data found for the given doctor_id.")
            return jsonify({"error": "No availability data found"}),  404

        dates = [{'date': row[0]} for row in date_data]
        print(dates)  # Print the availability data

        return jsonify(dates),  200
    except Exception as e:
        return jsonify({"error": str(e)}),  500
    
    
fetch_times_api_spec = {
    "description": "Fetch available times for a specific doctor on a specific date",
    "parameters": [
        {
            "name": "doctor_id",
            "in": "query",
            "required": "true",
            "type": "string",
            "description": "The ID of the doctor for which to fetch available times"
        },
        {
            "name": "date",
            "in": "query",
            "required": "true",
            "type": "string",
            "description": "The date for which to fetch available times"
        }
    ],
    "responses": {
        "200": {
            "description": "A list of available times for the specified doctor on the specified date",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "string",
                            "description": "The start time of the availability"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "The end time of the availability"
                        }
                    }
                }
            }
        },
        "404": {
            "description": "No availability data found for the given doctor_id and date",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
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


@fill_availability_bp.route('/fetch_times', methods=['GET'])
@jwt_required()
@swag_from(fetch_times_api_spec)
def fetch_time():
    print("fetch_times")
    doctor_id = request.args.get('doctor_id')  # Use request.args.get to get the doctor_id from query parameters
    dates = request.args.get('date')
    print(f"Received doctor_id: {doctor_id}", " Received date: {date}")
    try:
        from __init__ import mysql
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT start_time, end_time FROM doctor_availability WHERE Doc_ID = %s and Date_Available= %s", (doctor_id, dates,))
        time_data = cursor.fetchall()
        cursor.close()

        if not time_data:
            print("No availability data found for the given doctor_id.")
            return jsonify({"error": "No availability data found"}),  404

        times = [{'start_time': row[0],'end_time': row[1] } for row in time_data]
        print(times)  # Print the availability data

        return jsonify(times),  200
    except Exception as e:
        return jsonify({"error": str(e)}),  500
    
    
@fill_availability_bp.route('/appointment_history_details_patient', methods=['GET'])
@jwt_required()
def get_appointment_history():
    print("hello")
    try:
        # Assuming mysql connection is set up in __init__.py
        from __init__ import mysql
       
        # Get patient ID from query parameters
        user_id = request.args.get('user_id')
        print(f"Received user_id: {user_id}")
       
        # Connect to the database
        cursor = mysql.connection.cursor()
       
        # Query to fetch appointment history
        query = """
            SELECT u.Name AS Doctor_Name, a.appt_date, a.start_time, a.end_time, a.status
            FROM Appointment a
            JOIN users u ON a.Doc_ID = u.User_ID
            WHERE a.Patient_ID = %s and a.status='pending'
        """
       
        cursor.execute(query, (user_id,))
        appointment_history_data = cursor.fetchall()
       
        # Initialize a list to store appointment history
        appointment_history = []
       
        # Iterate over the fetched data and format it
        for appointment in appointment_history_data:
            # Since the date is already in 'yyyy-mm-dd' format, no conversion is needed
            formatted_appointment_date = appointment[1]
           
            # Create a dictionary for each appointment
            appointment_details = {
                'doctor_name': appointment[0],
                'appointment_date': formatted_appointment_date,
                'start_time': appointment[2],
                'end_time': appointment[3],
                'status': appointment[4]
            }
           
            # Append the appointment details to the list
            appointment_history.append(appointment_details)
            print(appointment_history)
        # Close the cursor
        cursor.close()
       
        # Return the appointment history as JSON response
        return jsonify({'appointment_history': appointment_history}), 200
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500



    
