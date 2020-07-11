from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField, validators
from app import db


# # Define the User data model. Make sure to add the flask_user.UserMixin !!
# class SingleProject(db.Model, UserMixin):
#     __tablename__ = 'projects'
#     id = db.Column(db.Integer, primary_key=True)
#
#     # User authentication information (required for Flask-User)
#     email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
#     email_confirmed_at = db.Column(db.DateTime())
#     password = db.Column(db.String(255), nullable=False, server_default='')
#     # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
#     active = db.Column(db.Boolean(), nullable=False, server_default='0')
#
#     # User information
#     active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
#     first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
#     last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
#
#     # Relationships
#     roles = db.relationship('Role', secondary='users_roles',
#                             backref=db.backref('users', lazy='dynamic'))


# Define the UserRoles association model
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    proj_title = db.Column(db.String(50))
    proj_desc = db.Column(db.String(255))
    proj_link = db.Column(db.String(1000))
    date_added = db.Column(db.Date)
    num_favorites = db.Column(db.Integer)

    # Relationships:
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))


class ProjectForm(FlaskForm):

    proj_title = StringField('Project Title', validators=[
        validators.DataRequired('Project Title is required.')])
    proj_desc = TextAreaField('Project description goes here.', validators=[
        validators.DataRequired('Project description is required.')])
    proj_link = StringField('Project Link', validators=[
        validators.URL('Must provide a valid URL.'),
        validators.DataRequired('Project Link is required.')
    ])
    submit = SubmitField('Save')


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
