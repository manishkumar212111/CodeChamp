
from flask import render_template,Flask
# from flask import jsonify
app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/template1')
def home():
    return render_template('template1.html')

@app.route('/template2')
def home():
    return render_template('template2.html')

# Uncomment to add a new URL at /new

# @app.route("/json")
# def json_message():
#     return jsonify(message="Hello World")
