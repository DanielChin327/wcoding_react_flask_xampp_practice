from flask import Flask, request, jsonify  # Import Flask core classes for creating the app, handling requests, and formatting JSON responses
from flask_cors import CORS                # Import CORS to handle Cross-Origin Resource Sharing
import sqlalchemy                          # Import SQLAlchemy for database operations

# Initialize a new Flask application instance
app = Flask(__name__)

# Enable cross-origin requests from the React frontend
CORS(app)

# Create a SQLAlchemy engine to connect to the MariaDB database
db = sqlalchemy.create_engine(
    "mariadb+pymysql://root:@localhost:3307/famous_quotesdb",  # Database connection string
    echo=True  # Enable SQL logging for debugging purposes
)

# Define a testing route for verifying the server is running
@app.route('/hello')  # Map the URL '/hello' to the home function
def home():
    return 'Hello There!'  # Return a simple greeting message

# Define a route to get all quotes
@app.route('/api/quotes', methods=['GET'])  # Handle GET requests to '/api/quotes'
def get_quote_route():
    quotes = get_quotes()  # Call the function to fetch quotes from the database
    if quotes is not None:
        return jsonify(quotes), 200  # Return the list of quotes as JSON with HTTP status 200 OK
    else:
        return jsonify({'error': 'Failed to retrieve quotes'}), 500  # Return an error message with HTTP status 500 Internal Server Error

# Define a route to add a new quote
@app.route('/api/quote', methods=['POST'])  # Handle POST requests to '/api/quote'
def add_quote_route():
    data = request.get_json()              # Parse the incoming JSON data from the request body
    person_name = data.get('person_name')  # Extract 'person_name' from the JSON data
    quote_text = data.get('quote')         # Extract 'quote' from the JSON data

    if add_quote(person_name, quote_text):  # Call the function to add the quote to the database
        return jsonify({'message': 'Quote successfully added'}), 200  # Return success message with HTTP status 200 OK
    else:
        return jsonify({'error': 'Failed to add quote'}), 500  # Return error message with HTTP status 500 Internal Server Error

# Define a route to delete a quote by its ID
@app.route('/api/quote/<int:quote_id>', methods=['DELETE'])  # Handle DELETE requests to '/api/quote/<quote_id>'
def delete_quote_route(quote_id):
    if delete_quote(quote_id):  # Call the function to delete the quote from the database
        return jsonify({'message': 'Quote successfully deleted'}), 200  # Return success message with HTTP status 200 OK
    else:
        return jsonify({'error': "Failed to delete"}), 500  # Return error message with HTTP status 500 Internal Server Error

# Function to fetch all quotes from the database
def get_quotes():
    try:
        with db.connect() as conn:  # Establish a connection to the database
            result = conn.execute(sqlalchemy.text('SELECT * FROM quotes'))  # Execute SQL query to select all records from 'quotes' table
            quotes = []  # Initialize an empty list to store quotes
            for row in result:  # Iterate over each row in the result set
                quotes.append({
                    'quotes_id': row[0],      # Extract 'quotes_id' (assuming it's the first column)
                    'person_name': row[1],    # Extract 'person_name' (assuming it's the second column)
                    'quote': row[2]           # Extract 'quote' (assuming it's the third column)
                })
        return quotes  # Return the list of quotes
    except Exception as err:
        print(f"Error fetching quotes: {err}")  # Print any exceptions that occur
        return None  # Return None to indicate failure

# Function to add a new quote to the database
def add_quote(person_name, quote_text):
    try:
        with db.connect() as conn:  # Establish a connection to the database
            insert_query = sqlalchemy.text(
                "INSERT INTO quotes (person_name, quote) VALUES (:person_name, :quote)"  # Prepare SQL insert statement with placeholders
            )
            conn.execute(insert_query, {"person_name": person_name, "quote": quote_text})  # Execute the insert statement with actual values
            conn.commit()  # Commit the transaction to save changes
        return True  # Return True to indicate success
    except Exception as err:
        print(f"Error adding quote: {err}")  # Print any exceptions that occur
        return False  # Return False to indicate failure

# Function to delete a quote from the database by its ID
def delete_quote(quote_id):
    try:
        with db.connect() as conn:  # Establish a connection to the database
            result = conn.execute(sqlalchemy.text(
                "DELETE FROM quotes WHERE quotes_id = :quote_id"  # Prepare SQL delete statement with placeholder
            ), {
                "quote_id": quote_id  # Bind the 'quote_id' parameter
            })
            conn.commit()  # Commit the transaction to save changes

            if result.rowcount > 0:
                return True  # Deletion was successful
            else:
                return False  # No rows were deleted; 'quote_id' may not exist
    except Exception as err:
        print(f"Error deleting quote: {err}")  # Print any exceptions that occur
        return False  # Indicate failure

# Run the Flask app in debug mode (useful for development)
if __name__ == '__main__':
    app.run(debug=True)
