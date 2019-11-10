from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField

class SignupForm(FlaskForm):
	name = StringField("Name: <font color=\"red\">*</font>", [validators.DataRequired()])
	email = EmailField("Email: <font color=\"red\">*</font>", [validators.DataRequired(), validators.Email()])
	password = PasswordField("Password: <font color=\"red\">*</font>", [validators.DataRequired()])
	password_conf = PasswordField("Confirm Password: <font color=\"red\">*</font>", [validators.DataRequired()])
	submit = SubmitField('Signup!')

class LoginForm(FlaskForm):
	email = EmailField("Email: <font color=\"red\">*</font>", [validators.DataRequired(), validators.Email()])
	password = PasswordField("Password: <font color=\"red\">*</font>", [validators.DataRequired()])
	submit = SubmitField('Login!')