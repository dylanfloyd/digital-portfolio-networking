from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, validators
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

    # Relationships:
    # creator_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    creator_id = db.Column(db.Integer(), db.ForeignKey('users.id'))




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
    title = StringField('Project Title', [
        DataRequired()])
    url = StringField('Project Link', [
        DataRequired(),
        URL(message=('Not a valid web address.'))])
    desc = StringField('Project Desc.', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    tags = StringField('#Specialization #Tags')

    submit = SubmitField('Submit')


# # Define the Role data model
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
#     label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes
#
#
# # Define the UserRoles association model
# class UsersRoles(db.Model):
#     __tablename__ = 'users_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
#
#
# # # Define the User registration form
# # # It augments the Flask-User RegisterForm with additional fields
# # class MyRegisterForm(RegisterForm):
# #     first_name = StringField('First name', validators=[
# #         validators.DataRequired('First name is required')])
# #     last_name = StringField('Last name', validators=[
# #         validators.DataRequired('Last name is required')])
#
#
# # Define the User profile form
# class UserProfileForm(FlaskForm):
#     first_name = StringField('First name', validators=[
#         validators.DataRequired('First name is required')])
#     last_name = StringField('Last name', validators=[
#         validators.DataRequired('Last name is required')])
#     submit = SubmitField('Save')
