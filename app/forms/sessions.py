from flask_wtf import FlaskForm
from wtforms import (
    IntegerField, SelectField,
    TextAreaField, DateTimeField,
    FieldList, FormField, Form,
    SubmitField, DecimalField,
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional


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
    weight = DecimalField(
        "Weight",
        validators=[
            Optional(),
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
            NumberRange(
                min=1,
                max=480,
                message="Duration must be less than 480 minutes."
            )
        ]
    )
    mode = SelectField(
        "Session Mode",
        choices=[
            ('online', 'Online'),
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
            Length(
                max=2048,
                message="Notes must be at most 2048 characters long."
            )
        ]
    )

    exercises = FieldList(
        FormField(AddSessionExerciseForm),
        min_entries=0,
        max_entries=30
    )
    submit = SubmitField("Add Session")


class AddSessionHelperForm(Form):
    exercises = FieldList(
        FormField(AddSessionExerciseForm),
        min_entries=0,
        max_entries=30
    )
