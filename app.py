from flask import Flask

app = Flask(__name__)


@app.route('/hello')
def home():
    return "hello there!"



if __name__ == "__main__":
    app.run(debug=True)
