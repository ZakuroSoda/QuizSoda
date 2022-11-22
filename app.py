from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', navBarPage="home")

@app.route('/login')
def login():
    return render_template('login.html', navBarPage="login")
    
@app.route('/register')
def register():
    return render_template('register.html', navBarPage="register")

@app.route('/challenges')
def challenge():
    return render_template('challengeGallery.html', navBarPage="challenges")

app.run(port=5000, host='0.0.0.0')