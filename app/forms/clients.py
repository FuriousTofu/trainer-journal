from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField,
    TextAreaField, SubmitField
)
from wtforms.validators import DataRequired, Length, NumberRange


class AddClientForm(FlaskForm):
    name = StringField(
        "Client Name",
        validators=[
            DataRequired(message="Client name is required."),
            Length(
                min=3,
                max=100,
                message="Client name must be 3 to 100 characters long."
            )
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
        choices=[
            ('active', 'Active'),
            ('pause', 'On Pause')
        ],
        default='active',
        validators=[DataRequired(message="Status is required.")]
    )
    contact = StringField(
        "Contact Information (Optional)",
        validators=[
            Length(
                max=100,
                message="Contact must be at most 100 characters long."
            )
        ]
    )
    notes = TextAreaField(
        "Notes (Optional)",
        validators=[
            Length(
                max=4096,
                message="Notes must be at most 4096 characters long."
            )
        ]
    )
    submit = SubmitField("Add Client")
