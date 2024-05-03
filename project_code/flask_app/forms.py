from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)

from .models import User

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")

class CommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")

class SquirrelReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )

    picture = FileField('Squirrel Picture', validators=[FileRequired(), FileAllowed(['png', 'jpg'], 'Images only!')])

    location_choices = [('', 'Select Location'), ('McKeldin Mall', 'McKeldin Mall'), ('Iribe', 'Iribe'), ('Morrill Quad', 'Morrill Quad'), ('South Campus', 'South Campus'), ('North Campus', 'North Campus'), ('Chapel Lawn', 'Chapel Lawn')]
    location = SelectField('Location', choices= location_choices, validators=[InputRequired()])

    submit = SubmitField("Submit Post")
    
class MovieReviewForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


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
        user1 = User.objects(extern_id=username.data).first()
        user2 = User.objects(username=username.data).first()
        if user1 or user2 is not None:
            raise ValidationError("Username is taken or someone else has that id")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


# TODO: implement fields
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

# TODO: implement
class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField('Update Username')

    # TODO: implement
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is already taken")

# TODO: implement
class UpdateProfilePicForm(FlaskForm):
    picture = FileField('Photo', validators = [FileRequired(), FileAllowed(['png', 'jpg'])])
    submit_picture = SubmitField('Upload')
