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
        coerce=str,  # Accept both IDs (as string) and new exercise names from TomSelect
        choices=[],
        validate_choice=False,  # Allow new values from TomSelect
        validators=[
            DataRequired(message="Exercise is required."),
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
        "Reps",
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
        "Starts at:",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired(message="Start date and time is required.")]
    )
    duration_min = IntegerField(
        "Duration (min.)",
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
        "Mode",
        choices=[
            ('online', 'Online'),
            ('offline', 'In-person')
        ],
        default='offline',
        validators=[DataRequired(message="Session mode is required.")]
    )
    price = IntegerField(
        "Price",
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
    submit = SubmitField("Add")

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
    submit = SubmitField("Save")

class SessionExercisesHelperForm(Form):
    exercises = FieldList(
        FormField(AddSessionExerciseForm),
        min_entries=0,
        max_entries=30
    )

