from flask import Flask, render_template, redirect, url_for, session, flash
from forms import LoginForm, SignupForm
from utils import login_required
import bcrypt
import models
from dotenv import load_dotenv
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login_handler():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		user_email, user_name, user_pwd_hash = models.load_user(email) # Get user data from database
		if user_email is None: # User not found
			flash('User not present please register')
			return redirect(url_for('signup_handler'))
		elif not bcrypt.checkpw(password.encode('utf8'), user_pwd_hash.encode('utf8')):
			flash('Incorrect Password!')
			return redirect(url_for('login_handler'))
		else:
			session['email'] = user_email # put email and name in session object
			session['name'] = user_name
		return redirect(url_for('home'))
		
	return render_template('login.html',form=form)


@app.route('/signup', methods=['GET','POST'])
def signup_handler():
	form = SignupForm()
	if form.validate_on_submit():
		name = form.name.data
		email = form.email.data
		password = form.password.data
		confirm_password = form.password_conf.data
		if password != confirm_password:
			return '<h1>Password do not match!</h1>'
		hashed_pwd = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()) # Hash Password with salt
		if bcrypt.checkpw(password.encode('utf8'), hashed_pwd):
			res = models.add_user(email, name, hashed_pwd) # Add user to DB
		if res:
			session['email'] = email # Add email and name to session object
			session['name'] = name
			return redirect(url_for('home'))
		else:
			return redirect(url_for('login_handler'))

	return render_template('signup.html',form=form)

@app.route('/home',methods=['GET','POST'])
@login_required # Custom decorator
def home():
	return render_template('home.html')

@app.route('/logout',methods=['GET'])
def logout_handler():
	session.pop('email') # Delete email and name from session object
	session.pop('name')
	return redirect(url_for('index'))

if __name__ == '__main__':
	env_path = Path('.') / '.env'
	load_dotenv(dotenv_path=env_path, verbose=True) # Load environment variables
	app.secret_key = os.getenv("SECRET_KEY")
	app.run(host='127.0.0.1', port=5000, debug=True)
