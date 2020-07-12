from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, URL

class NewProjectForm(FlaskForm):
    """Contact form."""
    title = StringField('Project Title', [
        DataRequired()])
    url = StringField('Project Link', [
        DataRequired(),
        URL(message=('Not a valid web address.'))])
    desc = TextAreaField('Message', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    submit = SubmitField('Submit')