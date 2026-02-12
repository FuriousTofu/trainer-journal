from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import ExerciseType


class ExerciseForm(FlaskForm):
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
    type = SelectField(
        "Type",
        choices=[(t.value, t.value.capitalize()) for t in ExerciseType],
        default=ExerciseType.REPS.name,
        validators=[DataRequired(message="Exercise type is required.")]
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


class AddExerciseForm(ExerciseForm):
    submit = SubmitField("Add")


class EditExerciseForm(ExerciseForm):
    submit = SubmitField("Save")
