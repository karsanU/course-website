from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

# Initialize app
app = Flask(__name__)


@app.route('/')
def prompt():
    if not session.get("logged_in"):
        return render_template("login.html")
    else: 
        return index()


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return prompt()

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

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return prompt()

 
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)