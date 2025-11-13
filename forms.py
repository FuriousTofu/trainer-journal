from flask_wtf import FlaskForm
from wtforms import (
    StringField, EmailField, PasswordField,
    SubmitField, BooleanField, TextAreaField,
    IntegerField, SelectField, DateTimeField,
    FieldList, FormField, Form,
)
from wtforms.validators import (
    DataRequired, Email, Length,
    EqualTo, Regexp, NumberRange,
)

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=25, message="Username must be between 3 and 25 characters."),
            Regexp('^[A-Za-z0-9._-]+$', message='Usernames must have only letters, digits, dot, underscore, dash.')
        ]
    )
    email = EmailField(
        'Email', 
        validators=[
            DataRequired(message="Email is required."),
            Length(max=120, message="Email must be at most 120 characters long."),
            Email(message="Invalid email address.")
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters long."),
            Length(max=1024, message="Ma man, please stop trying to DoS attack me.")
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
            Length(max=120, message="Email must be at most 120 characters long."),
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

class AddExerciseForm(FlaskForm):
    name = StringField(
        "Exercise Name",
        validators=[
            DataRequired(message="Exercise name is required."),
            Length(max=90, message="Exercise name must be at most 90 characters long.")
        ]
    )
    description = TextAreaField(
        "Description (Optional)",
        validators=[
            Length(max=1024, message="Description must be at most 1024 characters long.")
        ]
    )
    submit = SubmitField("Add Exercise")

class AddClientForm(FlaskForm):
    name = StringField(
        "Client Name",
        validators=[
            DataRequired(message="Client name is required."),
            Length(min=3, max=100, message="Client name must be 3 to 100 characters long.")
        ]
    )
    price = IntegerField(
        "Session Price",
        validators=[
            DataRequired(message="Session price is required."),
            NumberRange(min=1, message="Price must non-negative.")
        ]
    )
    status = SelectField(
        "Status",
        choices=[('active', 'Active'),
                 ('pause', 'On Pause'),
                 ('archive', 'Archived')
        ],
        default='active',
        validators=[DataRequired(message="Status is required.")]
    )
    contact = StringField(
        "Contact Information (Optional)",
        validators=[
            Length(max=100, message="Contact information must be at most 100 characters long.")
        ]
    )
    notes = TextAreaField(
        "Notes (Optional)",
        validators=[
            Length(max=4096, message="Notes must be at most 4096 characters long.")
        ]
    )
    submit = SubmitField("Add Client")

class AddSessionExerciseForm(Form):

    exercise = SelectField(
        "Exercise",
        coerce=int,
        validators=[
            DataRequired(message="Exercise is required."),
            NumberRange(min=1, message="Select an exercise.")
        ]
    )
    sets = IntegerField(
        "Sets",
        validators=[
            DataRequired(message="Number of sets is required."),
            NumberRange(min=1, message="There must be at least 1 set.")
        ]
    )
    reps = IntegerField(
        "Repetitions",
        validators=[
            DataRequired(message="Number of repetitions is required."),
            NumberRange(min=1, message="There must be at least 1 repetition.")
        ]
    )
    weight = IntegerField(
        "Weight",
        validators=[
            DataRequired(message="Weight is required."),
            NumberRange(min=0, message="Weight cannot be negative.")
        ]
    )

class AddSessionForm(FlaskForm):
    client = SelectField(
        "Client",
        coerce=int,
        validators=[
            DataRequired(message="Client selection is required."),
            NumberRange(min=1, message="Please select a client.")
        ]
    )
    start_dt = DateTimeField(
        "Start Date and Time",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired(message="Start date and time is required.")]
    )
    duration_min = IntegerField(
        "Duration (minutes)",
        default=60,
        validators=[
            DataRequired(message="Duration is required."),
            NumberRange(min=1, max=480, message="Duration must be less than 480 minutes.")
        ]
    )
    mode = SelectField(
        "Session Mode",
        choices=[('online', 'Online'),
                 ('offline', 'Offline')
        ],
        default='offline',
        validators=[DataRequired(message="Session mode is required.")]
    )
    price = IntegerField(
        "Session Price",
        validators=[
            DataRequired(message="Session price is required."),
            NumberRange(min=0, message="Price must be non-negative.")
        ]
    )
    notes = TextAreaField(
        "Notes (Optional)",
        validators=[
            Length(max=2048, message="Notes must be at most 2048 characters long.")
        ]
    )

    exercises = FieldList(FormField(AddSessionExerciseForm), min_entries=0, max_entries=30)
    submit = SubmitField("Add Session")
