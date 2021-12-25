from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    pass


class LoginForm(FlaskForm):
    
    phone_number = StringField("Telefon raqam", validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField("Parol", validators=[DataRequired()])
