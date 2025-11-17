from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class AddExerciseForm(FlaskForm):
    name = StringField(
        "Exercise Name",
        validators=[
            DataRequired(message="Exercise name is required."),
            Length(
                max=90,
                message="Exercise name must be at most 90 characters long."
            )
        ]
    )
    description = TextAreaField(
        "Description (Optional)",
        validators=[
            Length(
                max=1024,
                message="Description must be at most 1024 characters long."
            )
        ]
    )
    submit = SubmitField("Add Exercise")
