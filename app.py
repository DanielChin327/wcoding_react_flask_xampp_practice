from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import sqlalchemy

app = Flask(__name__)
CORS(app)  # To enable cross-origin requests from the React frontend

db = sqlalchemy.create_engine(
        "mariadb+pymysql://root:@localhost:3307/famous_quotesdb", echo=True
)


# Configure MySQL connection
db_config = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',  # replace with your MySQL username
    'password': '',  # replace with your MySQL password
    'database': 'famous_quotesdb'
}


# Testing routes
@app.route('/hello')
def home():
    return 'Hello There!'


# Route to handle saving quotes
@app.route('/api/save_quote', methods=['POST'])
def save_quote():
    data = request.json
    person_name = data.get('person_name')
    quote = data.get('quote')

    # Insert data into the database
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = "INSERT INTO quotes (person_name, quote) VALUES (%s, %s)"
        cursor.execute(insert_query, (person_name, quote))
        connection.commit()
        return jsonify({'message': 'Quote saved successfully!'}), 201
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': 'Failed to save quote'}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/quotes', methods=['GET'])
def get_quote():
    try:
        print("Attempting to connect to the database...")
        with db.connect() as conn:
            print("Connection successful!")
            result = conn.execute(sqlalchemy.text('SELECT quote FROM quotes'))
            quotes = [row['quote'] for row in result]
            print("Fetched Quotes:", quotes)
        return jsonify(quotes), 200
    except Exception as e:
        print("Error during database operation:", e)
        return jsonify({'error': 'Failed to retrieve quotes'}), 500









if __name__ == '__main__':
    app.run(debug=True)
