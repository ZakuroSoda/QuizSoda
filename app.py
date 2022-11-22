from flask import Flask, render_template, request, redirect, url_for
from hashlib import sha256

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', navBarPage="home")

@app.route('/login')
def login():
    return render_template('login.html', navBarPage="login")
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "GET":
        #if not logged in
        return render_template('register.html', navBarPage="register")
        #if logged in
            # redirect to home
    elif request.method == "POST":
        # since this application is meant to be small I really don't mind slapping all the validation here
        username, password, passwordConfirm = request.form['username'], request.form['password'], request.form['passwordConfirm']
        if password != passwordConfirm:
            return redirect(url_for('register')), 302 

@app.route('/challenges')
def challenge():
    return render_template('challengeGallery.html', navBarPage="challenges")

app.run(port=5000, host='0.0.0.0')
