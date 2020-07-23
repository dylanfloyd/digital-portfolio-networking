# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField
from app import db
from app.models.project_models import Project, ProjectLike
from wtforms.validators import DataRequired, Length, Email, URL

network = db.Table('network', db.Model.metadata,
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
                     )


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    username = db.Column(db.String(50), nullable=False, unique= True)
    # reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    bio = db.Column(db.Unicode(500), nullable=True, server_default=u'')
    interests = db.Column(db.Unicode(500), nullable=False, server_default='#Education #Technology #GT #OMSCS')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    projects = db.relationship('Project', backref=db.backref('creator', lazy=True))
    liked = db.relationship('ProjectLike', foreign_keys='ProjectLike.user_id', backref='user', lazy='dynamic')

    # following = db.relationship('Network', foreign_keys='Network.user_id',backref='user', lazy='dynamic')
    # followers = db.relationship('Network', backref='user', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=network,
        primaryjoin=(network.c.follower_id == id),
        secondaryjoin=(network.c.followed_id == id),
        backref=db.backref('network', lazy='dynamic'), lazy='dynamic')




    def like_project(self, project):
        if not self.has_liked_project(project):
            like = ProjectLike(user_id=self.id, project_id=project.id)
            db.session.add(like)

    def unlike_project(self, project):
        if self.has_liked_project(project):
            ProjectLike.query.filter_by(
                user_id=self.id,
                project_id=project.id).delete()

    def has_liked_project(self, project):
        return ProjectLike.query.filter(
            ProjectLike.user_id == self.id,
            ProjectLike.project_id == project.id).count() > 0


    def follow_user(self, user):
        if not self.has_followed_user(user):
            statement = network.insert().values(follower_id=self.id, followed_id=user.id)
            db.session.execute(statement)
            db.session.commit()
            #self.network.append(user)

    def unfollow_user(self, user):
        if self.has_followed_user(user):
            statement = network.delete().values(follower_id=self.id, followed_id=user.id)
            db.session.execute(statement)
            db.session.commit()
            #self.network.remove(user)

    def has_followed_user(self, user):
        self.network.filter(network.c.followed_id == user.id).count() > 0


        # abool = db.session.query(network).filter(network.c.follower_id==self.id and network.c.followed_id==user.id)
        # return abool ##db.session.query_property(db.exists().where((network.c.follower_id == self.id) & (network.c.followed_id == user.id)))
        # return User.query.join(network).join(User).filter((network.c.follower_id == self.id) & (network.c.followed_id == user.id)).count() > 0
        # return network.query.filter(network.c.follower_id == self.id, network.c.followed_id == user.id).count() > 0

    def followed_projects(self):
        return Project.query.join(
            network, (network.c.followed_id == Project.creator_id)).filter(
            network.c.follower_id == self.id).order_by(
            Project.date_added.desc())

# class ProjectLike(db.Model):
#     __tablename__ = 'project_like'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

# class Network(db.Model):
#     __tablename__ = 'network'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user_followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))



# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])


# Define the User profile form
class UserProfileForm(FlaskForm):


    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    bio = TextAreaField('Bio')
    interests = TextAreaField('#SpecializationInterests: ', validators=[
        DataRequired('Please enter at least one topic you are interested in. Dont forget to separate with spaces and start each interest with a # sign.')
    ])
    submit = SubmitField('Save')
