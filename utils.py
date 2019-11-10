from flask import session, url_for, redirect, flash
def login_required(func):
	"""Custom decorator for checking if the user is logged in or not
	Checks the session object
	"""
	def wrap_func():
			if 'email' not in session:
				flash("Please login to continue")
				return redirect(url_for('login_handler'))
			return func()
	wrap_func.__name__ = func.__name__
	return wrap_func