from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, IntegerField, SelectField,
    TextAreaField, DateTimeField,
    FieldList, FormField, Form,
    SubmitField, DecimalField,
)
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class AddSessionExerciseForm(Form):

    exercise = SelectField(
        "Exercise",
        coerce=lambda x: int(x) if x else 0, # Handle empty selection
        choices=[],
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

class SessionHeaderBaseForm(FlaskForm):
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
            ('offline', 'In-person')
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


class AddSessionForm(SessionHeaderBaseForm):
    client = SelectField(
        "Client",
        coerce=int,
        choices=[],
        validators=[
            DataRequired(message="Client selection is required."),
            NumberRange(min=1, message="Please select a client.")
        ]
    )
 
    exercises = FieldList(
        FormField(AddSessionExerciseForm),
        min_entries=0,
        max_entries=30
    )
    submit = SubmitField("Add Session")

class EditSessionForm(SessionHeaderBaseForm):
    status = SelectField(
        "Status",
        choices=[
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
            ("no_show", "No Show"),
        ],
        validators=[
            DataRequired(message="Status is required.")
        ]
    )
    is_paid = BooleanField("Paid?")
    submit = SubmitField("Save Changes")

class SessionExercisesHelperForm(Form):
    exercises = FieldList(
        FormField(AddSessionExerciseForm),
        min_entries=0,
        max_entries=30
    )

