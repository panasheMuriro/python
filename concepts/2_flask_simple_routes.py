from flask import Flask, request

app = Flask(__name__)

@app.route('/welcome', methods=['GET'])
def welcome():
    return "Welcome to the simple flask backend"
    
    
@app.route('/hello/<name>')
def greet_user(name):
    return f"hello {name}"



@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.json
    return f"Recived data: {data}", 200


if __name__ == '__main__':
    app.run(debug=True)