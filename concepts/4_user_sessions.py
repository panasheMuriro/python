
# Sessions are essential for creating user-specific experiences, such as maintaining login states or remembering user preferences.

# Lesson Goals
# Understand Sessions and Cookies
# Learn to Set Up Flask Sessions
# Use Sessions to Track User Logins
# Practice Clearing Session Data

# Sessions are used to store information for each user across multiple requests. 
# Flask sessions are stored on the client side as a cookie, and 
# Flask encrypts session data to ensure security.

# Example: If a user logs in, a session can store their login status so they don’t have to log in again on every page.


from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'jash273yh4br293rh42'


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    
    if not username:
        return "Username is required", 400
    
    session['username'] = username
    return f"Welcome, {username}! You are now logged in."


@app.route('/check_status')
def check_status():
    if 'username' in session:
        return f"User {session['username']} is logged in."
    
    return "User is not logged in"


@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return "You have been logged out."


@app.route('/visit')
def visit():
    # Check if 'visits' is in session; if not, initialize it
    if 'visits' in session:
        session['visits'] += 1
    else:
        session['visits'] = 1
    return f"This is your {session['visits']} visit!"

# we can reset all the data 
@app.route('/clear-session')
def clear_session():
    session.clear()
    return "Session cleared!"

if __name__ == "__main__":
    app.run(debug=True)