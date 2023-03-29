from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField,TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    staff = BooleanField('Staff Account?', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me', validators=[DataRequired()])
    submit = SubmitField('Login')


class HotelForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    capacity = IntegerField('Capacity', validators=[DataRequired()])
    peak_rate = IntegerField('Peak Rate', validators=[DataRequired()])
    off_peak_rate = IntegerField('Off Peak Rate', validators=[DataRequired()])
    available = BooleanField('Availablity', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Hotel')


