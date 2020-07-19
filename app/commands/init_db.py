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
from app.models.project_models import Project, ProjectLike

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
    generic_bio = "                About me section describing whatever the user wants to describe for their public profile. Example: OMSCS Grad student at Georgia Tech. Currently prototyping this application which you are examining. Words phrases sentences, etc. Words phrases sentences, etc. Words phrases sentences, etc. Words phrases sentences, etc. Words phrases sentences, etc..."
    # Create all tables
    db.create_all()
    db.session.commit()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    db.session.add(admin_role)
    db.session.commit()

    # Add users
    user1 = find_or_create_user(u'Admin',
                                u'Example',
                                u'administr8or',
                                u'admin@example.com',
                                'Password1',
                                admin_role,
                                u'This is the administrators bio. We run things around here')
    db.session.add(user1)
    db.session.commit()

    user2 = find_or_create_user(u'Member',
                                u'Example',
                                u'youser_demo',
                                u'member@example.com',
                                'Password1',
                                bio=generic_bio)
    db.session.add(user2)
    db.session.commit()

    user3 = find_or_create_user(u'Dylan',
                                u'Floyd',
                                u'dylanfloyd',
                                u'dfloyd7@gatech.edu',
                                'Password1',
                                bio=generic_bio)
    db.session.add(user2)
    db.session.commit()



    # Add dummy projects
    project1 = create_project(proj_title='Insignia-Prototype 1',
                             proj_desc='This first description is a placeholder for the Insignia-Prototype project.',
                             proj_link="https://www.google.com",
                             creator=user2 #user.id
                             )
    db.session.add(project1)
    db.session.commit()


    project2 = create_project(proj_title='Insignia-Prototype 2',
                             proj_desc='This second description is a placeholder for the Insignia-Prototype project.',
                             proj_link="https://www.facebook.com",
                             creator=user2 #user.id
                             )
    db.session.add(project2)
    db.session.commit()

    project3 = create_project(proj_title='Insignia-Prototype 3',
                             proj_desc='This third description is a placeholder for the Insignia-Prototype project.',
                             proj_link="https://www.twitter.com",
                             creator=user2 #user.id
                             )
    db.session.add(project3)
    db.session.commit()


    project4 = create_project(proj_title='Insignia-Prototype Web App',
                             proj_desc="Here's a link to the home page of the web app I created in my Ed Tech class."
                                       "It's a platform for sharing projects they are proud of and search for interesting projects "
                                       "of all kinds across all subjects to promote more personalized learning.",
                             proj_link="http://127.0.0.1:5000/",
                             creator=user3 #user.id
                             )
    db.session.add(project3)


    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, username, email, password, role=None, bio=''):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    active=True,
                    email_confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        if bio:
            user.bio=bio
        db.session.add(user)
    return user

def create_project(proj_title, proj_desc, proj_link, creator):
    """ Create new project """
    project = Project(proj_title=proj_title,
                      proj_desc=proj_desc,
                      proj_link=proj_link,
                      date_added=datetime.datetime.today(),
                      num_favorites=0,
                      creator=creator
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


