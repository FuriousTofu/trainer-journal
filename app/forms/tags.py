from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TagForm(FlaskForm):
    name = StringField(
        "Tag Name",
        validators=[
            DataRequired(message="Tag name is required."),
            Length(
                max=20,
                message="Tag name must be at most 20 characters long."
            )
        ]
    )
    color = StringField(
        "Color",
        validators=[DataRequired()],
        default="#6B7280"
    )


class AddTagForm(TagForm):
    submit = SubmitField("Add")


class EditTagForm(TagForm):
    submit = SubmitField("Save")
