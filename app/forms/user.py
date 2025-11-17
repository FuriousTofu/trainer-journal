from flask_wtf import FlaskForm
from wtforms import (
    StringField, EmailField, PasswordField,
    SubmitField, BooleanField
)
from wtforms.validators import (
    DataRequired, Email, Length,
    EqualTo, Regexp
)


class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(
                min=3,
                max=25,
                message="Username must be between 3 and 25 characters."
            ),
            Regexp(
                '^[A-Za-z0-9._-]+$',
                message=(
                    'Usernames must have only letters, '
                    'digits, dot, underscore, dash.'
                )
            )
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Length(
                max=120,
                message="Email must be at most 120 characters long."
            ),
            Email(message="Invalid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(
                min=8,
                message="Password must be at least 8 characters long."
            ),
            Length(
                max=1024,
                message="Ma man, please stop trying to DoS attack me."
            )
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            Length(max=1024, message="Nope, just don't."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Length(
                max=120,
                message="Email must be at most 120 characters long."
            ),
            Email(message="Invalid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(max=1024, message="That's too long, nope.")
        ]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
