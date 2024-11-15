# Using raw SQL can become cumbersome. 
# Flask-SQLAlchemy simplifies database operations by providing an Object-Relational Mapping (ORM) system.


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<User {self.name}>"
    
with app.app_context():
    db.create_all()

# db.create_all()
        

# CREATE
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"user created successfully"})

    
# READ
@app.route('/users', methods=['GET'])
def read_users():
    users = User.query.all()
    return jsonify([{"id":u.id, "name": u.name, "email": u.email} for u in users])

# UPDATE
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    
    if user:
        user.name = data["name"]
        user.email = data["email"]
        db.session.commit()
        
        return jsonify({"message": "User updated successfully"})
    return jsonify({"error":"user not found"})


# DELETE
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"messag": "user deleted successfuly"})
    return jsonify({"error": "user not found"}), 404

if __name__ =="__main__":
    app.run(debug=True)

    