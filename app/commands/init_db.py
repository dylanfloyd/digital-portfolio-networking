# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import User, Role
from app.models.project_models import Project

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')

def init_db():
    """ Initialize the database."""


    # db.session.remove()
    # db.session.commit()

    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()



    create_users()


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()
    db.session.commit()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')

    # Add users
    user = find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    user = find_or_create_user(u'Member', u'Example', u'member@example.com', 'Password1')
    # user = find_or_create_user(u'Dylan', u'Floyd', u'dylanfloyd@example.com', 'apwd')

    # Add dummy projects
    project = create_project(proj_title='Insignia-Prototype',
                             proj_desc='This description is a placeholder for the Insignia-Prototype project.',
                             proj_link="https://www.google.com",
                             cur_user=user.id
                             )

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def create_project(proj_title, proj_desc, proj_link, cur_user):
    """ Create new project """
    project = Project(proj_title=proj_title,
                      proj_desc=proj_desc,
                      proj_link=proj_link,
                      user_id=cur_user,
                      date_added=datetime.datetime.today(),
                      num_favorites=0
                      )
    db.session.add(project)
    return project

def find_project(proj_id):
    """ Find project """
    project = Project.query.filter(Project.id == proj_id).first()
    if not project:
        return -1
    else:
        return project


