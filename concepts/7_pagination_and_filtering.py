# Pagination

# Pagination is essential when you have a large set of data that would be inefficient to send all at once.
# Instead, we can break the data into smaller chunks (pages).
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app2.db'
db = SQLAlchemy(app)

fake = Faker()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
    def __repr__(self):
        return f"<User {self.name}>"

# Generate random users
def generate_random_users(num_users):
    for _ in range(num_users):
        user = User(name=fake.name(), email=fake.email())
        db.session.add(user)
    db.session.commit()

with app.app_context():
    db.create_all()
    # generate_random_users(50)


# PAGINATION
# Exmaple:  http://127.0.0.1:5000/users?page=2&per_page=10

@app.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    # users = User.query.paginate(page, per_page, False)
    users = User.query.paginate(page=page, per_page=per_page)

    return jsonify({
        'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })


# filtering 
@app.route('/users_filtered', methods=['GET'])
def get_users_filtered():
    """Get all users with pagination and filtering."""
    name_filter = request.args.get('name', '')
    email_filter = request.args.get('email', '')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = User.query
    
    if name_filter:
        query = query.filter(User.name.ilike(f"%{name_filter}%"))
    if email_filter:
        query = query.filter(User.email.ilike(f"%{email_filter}%"))
    
    users = query.paginate(page=page, per_page=per_page)
    return jsonify({
        'users': [{'id': user.id, 'name': user.name, 'email': user.email} for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })


if __name__ == "__main__":
    app.run(debug=True)
