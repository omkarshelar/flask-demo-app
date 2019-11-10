import mysql.connector
from flask import flash
import os

def add_user(email, name, password_hash):
	""" Adds user to the database
	returns True is operations was successful else logs the exception and returns false.
	"""
	received_email = load_user(email)
	if received_email is not None: # User with same email already present
		flash('User already present. Please Login')
		return 0
	try:
		db_password = os.getenv("DB_PASSWORD")
		cnx = mysql.connector.connect(user='test_user', password=db_password, database='demo_python')
		cursor = cnx.cursor()
		add_user = ('INSERT INTO users (email, name, password_hash) VALUES(%s, %s, %s)')
		data_user = (email, name, password_hash)
		cursor.execute(add_user, data_user)
		cnx.commit()
		cursor.close()
		cnx.close()
		return True
	except Exception as e:
		print(e)
		return False


def update_last_login(email):
	""" Update last login on user login
	"""
	try:
		db_password=os.getenv("DB_PASSWORD")
		cnx = mysql.connector.connect(user='test_user', password=db_password, database='demo_python')
		cursor = cnx.cursor()
		params = (email,)
		cursor.execute('UPDATE users SET last_login=NOW() WHERE email=%s', params)
		cnx.commit()
		cursor.close()
		cnx.close()
	except Exception as e:
		print(e)

def load_user(email):
	"""Gets user from the DB for a given email.
	Returns details of the user successfull on load
	Else returns None
	"""
	try:
		db_password = os.getenv("DB_PASSWORD")
		cnx = mysql.connector.connect(user='test_user', password=db_password, database='demo_python')
		cursor = cnx.cursor()
		params = (email,)
		cursor.execute('SELECT * FROM users WHERE email=%s', params)
		for(email, name, password_hash, last_login) in cursor:
			update_last_login(email)
			return email, name, password_hash, last_login
		return None, None, None, None
	except Exception as e:
		print(e)
		return None, None, None, None