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
    tags = StringField('#Specialization #Tags')

    submit = SubmitField('Submit')


# class ProjectForm(FlaskForm):
#
#     proj_title = StringField('Project Title', validators=[
#         validators.DataRequired('Project Title is required.')])
#     proj_desc = TextAreaField('Project Description', validators=[
#         validators.DataRequired('Project description is required.')])
#     proj_link = StringField('Project Link', validators=[
#         validators.URL('Must provide a valid URL.'),
#         validators.DataRequired('Project Link is required.')
#     ]),
#     proj_tags = StringField('#Specialization #Tags', validators=[
#         validators.DataRequired('At least one hashtag is required.')
#     ])
#     submit = SubmitField('Save')
