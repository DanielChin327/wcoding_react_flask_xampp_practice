from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlalchemy

app = Flask(__name__)
CORS(app)  # To enable cross-origin requests from the React frontend

db = sqlalchemy.create_engine(
    "mariadb+pymysql://root:@localhost:3307/famous_quotesdb", echo=True
)

# Testing route
@app.route('/hello')
def home():
    return 'Hello There!'

# GET quotes
@app.route('/api/quotes', methods=['GET'])
def get_quote_route():
    quotes = get_quotes()
    if quotes is not None:
        return jsonify(quotes), 200
    else:
        return jsonify({'error': 'Failed to retrieve quotes'}), 500

# Add a quote
@app.route('/api/quote', methods=['POST'])
def add_quote_route():
    data = request.get_json()
    person_name = data.get('person_name')
    quote_text = data.get('quote')

    if add_quote(person_name, quote_text):
        return jsonify({'message': 'Quote successfully added'}), 200
    else:
        return jsonify({'error': 'Failed to add quote'}), 500

def get_quotes():
    try:
        with db.connect() as conn:
            result = conn.execute(sqlalchemy.text('SELECT person_name, quote FROM quotes'))
            quotes = [{"person_name": row['person_name'], "quote": row['quote']} for row in result]
        return quotes
    except Exception as err:
        print(f"Error fetching quotes: {err}")
        return None  # Indicate failure

def add_quote(person_name, quote_text):
    try:
        with db.connect() as conn:
            insert_query = sqlalchemy.text(
                "INSERT INTO quotes (person_name, quote) VALUES (:person_name, :quote)"
            )
            conn.execute(insert_query, {"person_name": person_name, "quote": quote_text})
            conn.commit()
        return True  # Indicate success
    except Exception as err:
        print(f"Error adding quote: {err}")
        return False  # Indicate failure

if __name__ == '__main__':
    app.run(debug=True)
