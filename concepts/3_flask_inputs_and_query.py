# Lesson Goals
# Understand POST Requests
# Learn to Handle Form Data with POST
# Practice Parsing JSON Data from POST Requests

from flask import Flask, request, jsonify

#  passing small amounts of data with the '?variable=data'

app = Flask(__name__)

@app.route('/search')
def search():
    query = request.args.get('query')
    category = request.args.get('category')
    
    if query and category:
        return f"Searching results for {query} in {category}"
    elif query:
        return f"Searching results for : {query}"
    else:
        return "No search term provided"


# form data

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        return f"Loged in as {username}", 200
    
    else:
        return "Username or password invalid"


#  json data
@app.route('/submit_feedback', methods=['POST'])
def json_submit():
    data= request.get_json()
    if 'name' not in data or 'feedback' not in data:
        return jsonify({"error": "Name and feedback is required"}), 400
    else:
        return jsonify({"message": f"Thank you {data['name']} for your feedback {data['feedback']}"})


if __name__ == "__main__":
    app.run(debug=True)