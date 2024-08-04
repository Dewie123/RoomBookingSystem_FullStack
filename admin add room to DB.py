from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import mysql.connector


app = Flask(__name__,template_folder='templates')
CORS(app)
# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'tkyk7777',
    'database': 'admin_added_room_list',
}

@app.route('/api/insert', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()  # Get JSON data 

        target_table = data.get('target-table', 'admin_room_table')
        if target_table == 'admin_room_table':
            room_name = data.get('room-name', 'Your Room Name')
            room_type = data.get('room-type', 'Your Room Type')
            room_desc = data.get('room-desc', 'Your Room Description')
            room_capacity = data.get('room-capacity', 'Your Room Capacity')
            room_start_date = data.get('room-start-date', '2023-10-16')
            room_end_date = data.get('room-end-date', '2023-10-18')
            room_duration = data.get('room-duration', '08:00-10:00')
            room_price = data.get('room-price', '5')
            room_image = data.get('room-image', 'path_to_image.jpg')

            # Insert data into the admin_room_table
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            insert_query = "INSERT INTO admin_room_table (room_name, room_type, room_desc, room_capacity, room_start_date, room_end_date, room_duration, room_price, room_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (room_name, room_type, room_desc, room_capacity, room_start_date, room_end_date, room_duration, room_price, room_image)
            cursor.execute(insert_query, data)
            db.commit()
            cursor.close()
            db.close()
            response = {'message': 'Data inserted successfully'}
            return jsonify(response), 200

        elif target_table == 'promo_codes':
            # Handle data insertion into the promo_codes table
            promo_code = data.get('promo-code', 'Your Promo Code')
            promo_start_date = data.get('promo-start-date', '2023-10-16')
            promo_end_date = data.get('promo-end-date', '2023-10-18')
            promo_amount = data.get('promo-amount', '0.00')

            # Insert data into the promo_codes table
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            insert_query = "INSERT INTO promo_codes (promo_code, promo_start_date, promo_end_date, promo_amount) VALUES (%s, %s, %s, %s)"
            data = (promo_code, promo_start_date, promo_end_date, promo_amount)
            cursor.execute(insert_query, data)
            db.commit()
            cursor.close()
            db.close()
            response = {'message': 'Promo code data inserted successfully'}
            return jsonify(response), 200

        elif target_table == 'student_room_table':
            room_name = data.get('room-name', 'Your Room Name')
            room_start_date = data.get('room-start-date', '2023-10-16')
            room_duration = data.get('room-duration', '08:00-10:00')

            # Insert data into the admin_room_table
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            insert_query = "INSERT INTO student_room_table (room_name, room_start_date, room_duration) VALUES (%s, %s, %s)"
            data = (room_name,room_start_date,room_duration)
            cursor.execute(insert_query, data)
            db.commit()
            cursor.close()
            db.close()
            response = {'message': 'Data inserted successfully'}
            return jsonify(response), 200

        else:
            response = {'error': 'Invalid target-table value'}
            return jsonify(response), 400

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

#combining insert1 and insert2 endpoints
@app.route('/api/insert3', methods=['POST'])
def insert_data3():
    try:
        data = request.get_json()  # Get JSON data from the request

        room_name = data.get('room_name', 'Your Room Name')
        room_start_date = data.get('room_start_date', '2023-10-16')
        room_duration = data.get('room_duration', '08:00-10:00')
        promo_code = data.get('promo_code', 'PROMO1')

        # Insert data into the student_room_table
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Insert data into the student_room_table
        print("insert query")
        insert_query = "INSERT INTO student_room_table (room_name, room_start_date, room_duration, promo_code) VALUES (%s, %s, %s, %s)"
        data = (room_name, room_start_date, room_duration, promo_code)
        cursor.execute(insert_query, data)
        db.commit()


        # Check if the same "room_name" exists in both student_room_table and admin_room_table
        cursor.execute("SELECT COUNT(*) FROM student_room_table WHERE room_name = %s", (room_name,))
        student_exists = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM admin_room_table WHERE room_name = %s", (room_name,))
        admin_exists = cursor.fetchone()[0]

        #  Check if the same "promo_code" exists in both student_room_table and promo_codes
        cursor.execute("SELECT COUNT(*) FROM student_room_table WHERE promo_code = %s", (promo_code,))
        student_promo_exists = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM promo_codes WHERE promo_code = %s", (promo_code,))
        promo_exists = cursor.fetchone()[0]

        if student_exists and admin_exists and student_promo_exists and promo_exists:
            #  Retrieve "promo_amount" and "room_price"
            cursor.execute("SELECT promo_amount FROM promo_codes WHERE promo_code = %s", (promo_code,))
            promo_amount = cursor.fetchone()[0]
            cursor.execute("SELECT room_price FROM admin_room_table WHERE room_name = %s", (room_name,))
            room_price = cursor.fetchone()[0]

            #  Calculate the new "room_price"
            new_room_price = room_price - promo_amount
            print(new_room_price)
            #  Update the "room_price" in the "admin_room_table"
            cursor.execute("UPDATE admin_room_table SET room_price = %s WHERE room_name = %s", (new_room_price, room_name))
            db.commit()

        # Insert data into the student_room_table
        #print("insert query")
        #insert_query = "INSERT INTO student_room_table (room_name, room_start_date, room_duration, promo_code) VALUES (%s, %s, %s, %s)"
        #data = (room_name, room_start_date, room_duration, promo_code)
        #cursor.execute(insert_query, data)
        #db.commit()

        cursor.close()
        db.close()
        response = {'message': 'Data inserted successfully'}

        return jsonify(response), 200

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500



@app.route('/api/insert1', methods=['POST'])
def insert_data1():
    try:
        data = request.get_json()  # Get JSON data from the request

        room_name = data.get('room_name','Your Room Name')
        room_start_date = data.get('room_start_date', '2023-10-16')
        room_duration = data.get('room_duration', '08:00-10:00')
        promo_code = data.get('promo_code', 'PROMO1')

        # Insert data into the admin_room_table
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        insert_query = "INSERT INTO student_room_table (room_name, room_start_date, room_duration,promo_code) VALUES (%s, %s, %s, %s)"
        data = (room_name,room_start_date,room_duration,promo_code)
        print(data)
        cursor.execute(insert_query, data)
        db.commit()
        cursor.close()
        db.close()
        response = {'message': 'Data inserted successfully'}
        
        return jsonify(response), 200


    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500



@app.route('/api/insert2', methods=['POST'])
def use_promo():
    try:
        data = request.get_json()  # Get JSON data from the request

        room_name = data.get('room_name', 'Your Room Name')
        room_start_date = data.get('room_start_date', '2023-10-16')
        room_duration = data.get('room_duration', '08:00-10:00')
        promo_code = data.get('promo_code', 'PROMO1')

        # Insert data into the student_room_table
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        #  Check if the same "room_name" exists in both student_room_table and admin_room_table
        cursor.execute("SELECT COUNT(*) FROM student_room_table WHERE room_name = %s", (room_name,))
        student_exists = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM admin_room_table WHERE room_name = %s", (room_name,))
        admin_exists = cursor.fetchone()[0]

        #  Check if the same "promo_code" exists in both student_room_table and promo_codes
        cursor.execute("SELECT COUNT(*) FROM student_room_table WHERE promo_code = %s", (promo_code,))
        student_promo_exists = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM promo_codes WHERE promo_code = %s", (promo_code,))
        promo_exists = cursor.fetchone()[0]

        if student_exists and admin_exists and student_promo_exists and promo_exists:
            # Retrieve "promo_amount" and "room_price"
            cursor.execute("SELECT promo_amount FROM promo_codes WHERE promo_code = %s", (promo_code,))
            promo_amount = cursor.fetchone()[0]
            cursor.execute("SELECT room_price FROM admin_room_table WHERE room_name = %s", (room_name,))
            room_price = cursor.fetchone()[0]

            #  Calculate the new "room_price"
            new_room_price = room_price - promo_amount
            print(new_room_price)
            #  Update the "room_price" in the "admin_room_table"
            cursor.execute("UPDATE admin_room_table SET room_price = %s WHERE room_name = %s", (new_room_price, room_name))
            db.commit()


        cursor.close()
        db.close()

        response = {'message': 'Data inserted successfully'}

        return jsonify(response), 200

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500



@app.route('/display_student_room_dropdown')
def display_student_room_dropdown():
    try:
        # Create a connection to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor to execute SQL queries
        cursor = db.cursor()

        # Fetch room names
        room_query = "SELECT room_name FROM admin_room_table"
        cursor.execute(room_query)
        room_data = cursor.fetchall()

        query = "SELECT room_name, room_type, room_desc, room_capacity, room_start_date, room_end_date, room_duration, room_price, room_image, Available_to_book FROM admin_room_table"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        db.close()

        # Pass room names, booking dates, and time slots to the HTML template for rendering
        return render_template('Student add room.html', room_names=room_data , rooms=data)
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500




@app.route('/display_student_rooms')
def display_student_room():
    try:
        
        db = mysql.connector.connect(**db_config)

       
        cursor = db.cursor()

        
        query = "SELECT room_name, room_type, room_desc, room_capacity, room_start_date, room_end_date, room_duration, room_price, room_image, Available_to_book FROM admin_room_table"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        db.close()
        # Pass the data to the HTML template for rendering
        return render_template('Student view room.html', rooms=data)
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

@app.route('/display_rooms')
def display_promo():
    try:
        
        db = mysql.connector.connect(**db_config)

        
        cursor = db.cursor()

        
        query = "SELECT room_name, room_type, room_desc, room_capacity, room_start_date, room_end_date, room_duration, room_price, room_image, Available_to_book FROM admin_room_table"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        db.close()
        # Pass the data to the HTML template for rendering
        return render_template('Admin view room.html', rooms=data)
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

@app.route('/display_promo')
def display_rooms():
    try:
        
        db = mysql.connector.connect(**db_config)

        
        cursor = db.cursor()

        
        query = "SELECT promo_code, promo_start_date, promo_end_date, promo_amount FROM promo_codes"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        db.close()
        # Pass the data to the HTML template for rendering
        return render_template('Admin view promo.html', rooms=data)
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

#from Student add room .html
@app.route('/student_view_room')
def student_view_room():
    try:
        
        db = mysql.connector.connect(**db_config)

       
        cursor = db.cursor()

       
        query = """
        SELECT a.*, s.room_start_date AS student_start_date, s.room_duration AS student_duration
        FROM admin_room_table a
        INNER JOIN student_room_table s ON a.room_name = s.room_name
        """
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        db.close()

        # Pass the data to the HTML template for rendering
        return render_template('Student view room.html', rooms=data)
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500
    

@app.route('/delete_booking', methods=['DELETE'])
def delete_booking():
    try:
        data = request.get_json()  

        room_name = data.get('room_name', None)  

        if room_name is not None:
           
            db = mysql.connector.connect(**db_config)

           
            cursor = db.cursor()

            # DELETE SQL query to remove the booking with the specified room_name
            delete_query = "DELETE FROM student_room_table WHERE room_name = %s"
            data = (room_name,)

            cursor.execute(delete_query, data)
            db.commit()

            cursor.close()
            db.close()

            response = {'message': 'Booking deleted successfully'}
            return jsonify(response), 200
        else:
            response = {'error': 'Room name not provided for deletion'}
            return jsonify(response), 400

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500


# Update the admin_room_table based on the room name
def update_admin_room_table(room_name, new_booking_date, new_room_duration):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    
    update_query = """
    UPDATE admin_room_table
    SET room_start_date = %s, room_duration = %s
    WHERE room_name = %s
    """
    
    data = (new_booking_date, new_room_duration, room_name)
    cursor.execute(update_query, data)
    db.commit()
    
    cursor.close()
    db.close()

# Update student_room_table based on the room name
def update_student_room_table(room_name, new_booking_date, new_room_duration):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    
    update_query = """
    UPDATE student_room_table
    SET room_start_date = %s, room_duration = %s
    WHERE room_name = %s
    """
    
    data = (new_booking_date, new_room_duration, room_name)
    cursor.execute(update_query, data)
    db.commit()
    
    cursor.close()
    db.close()


@app.route('/process_and_display_data', methods=['POST'])
def process_and_display_data():
    try:
        
        data = request.get_json()
        room_name = data.get('room_name')
        print("Received room_name:", room_name)  
        global x 
        x = room_name
       
        return render_template('Student view room edit.html', room_name=room_name)

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

@app.route('/student_view_room_edit')
def student_view_room_edit():
    try:
       
        room_name = request.args.get('room_name') 
        print("Received room_name:", room_name)   
        print("Received room_name:", x)  
        return render_template('Student view room edit.html', room_name=x)  

    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500
    
@app.route('/api/update_booking', methods=['POST'])
def update_booking():
    try:
        data = request.get_json()
       
        room_name = data.get('room_name')
        room_start_date = data.get('room_start_date')
        room_duration = data.get('room_duration')

        print(f"Received room_name: {room_name}")
        print(f"Received room_start_date: {room_start_date}")
        print(f"Received room_duration: {room_duration}")
        
        db = mysql.connector.connect(**db_config)

        
        cursor = db.cursor()

        
        update_query = "UPDATE student_room_table SET room_start_date = %s, room_duration = %s WHERE room_name = %s"
        update_query2 = "UPDATE admin_room_table SET room_start_date = %s, room_duration = %s WHERE room_name = %s"
        data = (room_start_date, room_duration, room_name)

        cursor.execute(update_query, data)
        cursor.execute(update_query2, data)
        db.commit()

        cursor.close()
        db.close()

        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        error_message = str(e)
        response = {'error': error_message}
        return jsonify(response), 500

@app.route('/admin_add_room')
def add_room_page():
    return send_from_directory('static', 'Admin add room.html')

@app.route('/admin_add_promo')
def add_promo_page():
    return send_from_directory('static', 'Admin add promo.html')

@app.route('/RBS')
def RBS():
    return send_from_directory('static','RBS.html')

@app.route('/admin_login_page')
def admin_login_page():
    return send_from_directory('static','Admin login page.html')
    
@app.route('/student_login_page')
def student_login_page():
    return send_from_directory('static','Student login page.html')


if __name__ == '__main__':
    app.run(debug=True)  

