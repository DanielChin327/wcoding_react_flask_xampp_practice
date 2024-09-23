from flask import Flask, request, jsonify  # Import necessary Flask modules for creating the app, handling requests, and formatting JSON responses
from flask_cors import CORS               # Import CORS to handle Cross-Origin Resource Sharing
import sqlalchemy                         # Import SQLAlchemy for database operations

app = Flask(__name__)   # Initialize a new Flask application instance
CORS(app)               # Enable cross-origin requests from the React frontend

# Create a SQLAlchemy engine to connect to the MariaDB database
db = sqlalchemy.create_engine(
    "mariadb+pymysql://root:@localhost:3307/famous_quotesdb", echo=True  # Database connection string with echo enabled for SQL logging
)

# Define a testing route
@app.route('/hello')    # Decorator that maps the URL '/hello' to the home function
def home():
    return 'Hello There!'  # Return a simple greeting message

# Define a route to get all quotes
@app.route('/api/quotes', methods=['GET'])  # Route that handles GET requests to '/api/quotes'
def get_quote_route():
    quotes = get_quotes()  # Call the function to fetch quotes from the database
    if quotes is not None:
        return jsonify(quotes), 200  # Return the list of quotes in JSON format with HTTP status 200 OK
    else:
        return jsonify({'error': 'Failed to retrieve quotes'}), 500  # Return an error message with HTTP status 500 Internal Server Error

# Define a route to add a new quote
@app.route('/api/quote', methods=['POST'])  # Route that handles POST requests to '/api/quote'
def add_quote_route():
    data = request.get_json()              # Parse the incoming JSON data from the request body
    person_name = data.get('person_name')  # Extract 'person_name' from the JSON data
    quote_text = data.get('quote')         # Extract 'quote' from the JSON data

    if add_quote(person_name, quote_text):  # Call the function to add the quote to the database
        return jsonify({'message': 'Quote successfully added'}), 200  # Return a success message with HTTP status 200 OK
    else:
        return jsonify({'error': 'Failed to add quote'}), 500  # Return an error message with HTTP status 500 Internal Server Error


@app.route('/api/quote/<int:quote_id>', methods = ['DELETE'])
def delete_quote_route(quote_id):
    if delete_quote(quote_id):
        return jsonify({'message': 'Quote successfully deleted'}),200
    else:
        return jsonify({'error': "Failed to delete"}),500





def get_quotes():
    try:
        with db.connect() as conn:  # Establish a connection to the database
            result = conn.execute(sqlalchemy.text('SELECT * FROM quotes'))  # Execute an SQL query to select all records from the 'quotes' table
            quotes = []
            for row in result:       # Iterate over the result set
                quotes.append({
                    'quotes_id': row[0],
                    'person_name': row[1],  # Extract 'person_name' from the row (assuming it's the second column)
                    'quote': row[2]         # Extract 'quote' from the row (assuming it's the third column)
                })
        return quotes  # Return the list of quotes
    except Exception as err:
        print(f"Error fetching quotes: {err}")  # Print any exceptions that occur during the database operation
        return None  # Return None to indicate failure

def add_quote(person_name, quote_text):
    try:
        with db.connect() as conn:  # Establish a connection to the database
            insert_query = sqlalchemy.text(
                "INSERT INTO quotes (person_name, quote) VALUES (:person_name, :quote)"  # Prepare an SQL insert statement with placeholders
            )
            conn.execute(insert_query, {"person_name": person_name, "quote": quote_text})  # Execute the insert statement with actual values
            conn.commit()  # Commit the transaction to save changes
        return True  # Return True to indicate success
    except Exception as err:
        print(f"Error adding quote: {err}")  # Print any exceptions that occur during the database operation
        return False  # Return False to indicate failure


def delete_quote(quote_id):
    try:
        with db.connect() as conn:
            delete_query = sqlalchemy.text(
                "DELETE FROM quotes WHERE id = :quotes_id"
            )
            result = conn.execute(delete_query, {"quotes_id": quote_id})
            conn.commit()

            if result.rowcount > 0:
                return True  # Deletion was successful
            else:
                return False  # No rows affected; quote_id may not exist
    except Exception as err:
        print(f"Error deleting quote: {err}")
        return False  # Indicate failure


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode (useful for development)
