
# Validation is essential to ensure that your data is clean, consistent, and adheres to your application's requirements before processing or storing it. 
# Let’s explore how to handle validation in your Flask application.
# Adding Validation to User Input
# We can use Flask libraries like marshmallow, pydantic, or even plain Python checks to validate incoming requests. 
# Here's how you can add validation for user data when creating a user.

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate, ValidationError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<User {self.name}>"
    
    
class UserSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)

user_schema = UserSchema()

    
with app.app_context():
    db.create_all()
    
@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Validate input data
        data = user_schema.load(request.json)
        # If validation passes, create a user
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created!', 'user': user_schema.dump(new_user)}), 201
    except ValidationError as e:
        # Return validation errors
        return jsonify({'errors': e.messages}), 400

if __name__ == "__main__":
    app.run(debug=True)
    
    
"""
OUTPUT


- Invalid

{
    "errors": {
        "email": [
            "Not a valid email address."
        ],
        "name": [
            "Length must be between 3 and 80."
        ]
    }
}


- Valid

{
    "message": "User created!",
    "user": {
        "email": "p@gmail.com",
        "name": "panashe"
    }
}

"""