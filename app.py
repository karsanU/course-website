from flask import Flask, render_template, request, make_response
from functools import wraps
from flask_wtf import FlaskFrom
app = Flask(__name__)




@app.route('/')
@app.route('/index.html')
def index():
    return  render_template("index.html")

@app.route('/news.html')
def news():
    return  render_template("news.html")

@app.route('/lectures.html')
def lectures():
    return  render_template("lectures.html")

@app.route('/labs.html')
def labs():
    return  render_template("labs.html")

@app.route('/contacts.html')
def contact():
    return  render_template("contacts.html")

@app.route('/assignments.html')
def assignments():
    return  render_template("assignments.html")

 
if __name__ == '__main__':
    app.run(debug=True)