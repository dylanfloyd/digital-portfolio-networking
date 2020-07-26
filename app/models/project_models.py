from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, RadioField, validators
from app import db
from datetime import datetime
from wtforms.validators import DataRequired, Length, Email, URL





# Define the UserRoles association model
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    proj_title = db.Column(db.String(50), nullable=False)
    proj_desc = db.Column(db.String(255), nullable=False)
    proj_link = db.Column(db.String(1000), nullable=False, default="https://www.google.com")
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    num_favorites = db.Column(db.Integer, nullable=False, default=0)
    proj_tags = db.Column(db.String(1000), nullable=True, default="#Project #Tags")
    privacy_setting = db.Column(db.String(20), nullable=False, default="PUBLIC") #OPTIONS: ["PUBLIC", "NETWORK", "PRIVATE"]

    # Relationships:
    # creator_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    creator_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    likes = db.relationship('ProjectLike', backref='project', lazy='dynamic')

class ProjectLike(db.Model):
    __tablename__ = 'project_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


class EditProjectForm(FlaskForm):


    title = StringField('Project Title: ', [
        DataRequired()])
    url = StringField('Project Link: ', [
        DataRequired(),
        URL(message=('Not a valid web address.'))])
    desc = TextAreaField('Project Desc: ', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    tags = StringField('#Specialization #Tags: ')
    privacy = RadioField('Visible To: ', choices=[('PUBLIC','PUBLIC'), ('NETWORK','NETWORK'), ('PRIVATE','PRIVATE')], default="PUBLIC", coerce=str)

    delete = SubmitField('Delete Project')

    # title = StringField('Project Title', validators=[
    #     validators.DataRequired('Project Title is required.')])
    # desc = TextAreaField('Project Description', validators=[
    #     validators.DataRequired('Project description is required.')])
    # url = StringField('Project Link', validators=[
    #     validators.URL('Must provide a valid URL.'),
    #     validators.DataRequired('Project Link is required.')
    # ]),
    # tags = StringField('#Specialization #Tags', validators=[
    #     validators.DataRequired('At least one hashtag is required.')
    # ])
    submit = SubmitField('Save')


class NewProjectForm(FlaskForm):
    """Contact form."""
    title = StringField('Project Title: ', [
        DataRequired()])
    url = StringField('Project Link: ', [
        DataRequired(),
        URL(message=('Not a valid web address.'))])
    desc = TextAreaField('Project Desc: ', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    tags = StringField('#Specialization #Tags: ')
    # privacy = RadioField('Visible To: ', choices=[(1,'PUBLIC'), (2,'NETWORK'), (3,'PRIVATE')], default=1, coerce=int)
    privacy = RadioField('Visible To: ', choices=[('PUBLIC','PUBLIC'), ('NETWORK','NETWORK'), ('PRIVATE','PRIVATE')], default="PUBLIC", coerce=str)
    submit = SubmitField('Submit')


class ProjectSearchForm(FlaskForm):
    searchbar = StringField('')
    submit = SubmitField('Submit')



