from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User


class TagSearch(FlaskForm):
    search_query = StringField(
        "Tag", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submitT = SubmitField("Search Tags")


class NameSearch(FlaskForm):
    search_query = StringField(
        "Name", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submitN = SubmitField("Search for Name")


class PostForm(FlaskForm):
    text = TextAreaField(
        "PostText", validators=[InputRequired(), Length(min=1, max=1000)]
    )
    tag = StringField(
        "Tag", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Post")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")