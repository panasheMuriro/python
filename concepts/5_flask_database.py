# Lesson Goals
# Understand Database Basics
# Set Up SQLite with Flask
# Perform CRUD Operations (Create, Read, Update, Delete)
# Use Flask-SQLAlchemy for ORM
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "db_2.db"

def  get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row # return rows as dictionaries
    return conn

# initialize the table

@app.before_first_request
def initialize_table():
    conn = get_db_connection()
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE 
                 )
                 """)
    conn.commit()
    conn.close()
    
# CREATE USER
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    
    conn = get_db_connection()
    
    conn.execute("INSERT INTO users (name,email) VALUES (?,?)", (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"User {name} created successfully"})
    
    
# READ USERS
@app.route('/users', methods=['GET'])
def read_users():
    conn = get_db_connection()
    
    users = conn.execute("SELECT * FROM users").fetchall()
    # users = conn.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])
    
    
#  READ SPECIFIC USER

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(dict(user))
    
    
#  UPDATE with PUT
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    
    conn = get_db_connection()
    conn.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "updated user successfully"})


#  DELETE user

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "users deleted successfully"})


     
if __name__ =="__main__":
    app.run(debug=True)

