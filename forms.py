import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,EmailField,SubmitField,URLField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor
number_seats = ("0-10","10-20","20-30","30-40","40-50","50+")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddcityForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    map_url = URLField("Map Url",validators=[DataRequired()])
    img_url = URLField("Img Url",validators=[DataRequired()])
    location = StringField("Location",validators=[DataRequired()])
    has_sockets = StringField("Sockets",validators=[DataRequired()])
    has_toilet = StringField("Toilets",validators=[DataRequired()])
    has_wifi = StringField("Wifi",validators=[DataRequired()])
    can_take_calls = StringField("Can take calls",validators=[DataRequired()])
    seats = wtforms.SelectField("Number of seats", choices= number_seats)
    coffe_price = StringField("Coffe price",validators=[DataRequired()])
    submit = SubmitField("Submit")
