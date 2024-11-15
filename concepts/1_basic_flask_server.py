from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask Development Simple Server"


if __name__ == '__main__':
    app.run(debug=True)