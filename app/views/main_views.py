# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm
from app.models.project_models import ProjectForm, Project
from forms import NewProjectForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')
# project_blueprint = Blueprint('project', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/user_profile_page.html', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html', form=form)


@main_blueprint.route('/main/portfolio', methods=['GET', 'POST'])
@login_required
def user_portfolio_page():
    # # Initialize form
    # form = UserProfileForm(request.form, obj=current_user)
    #
    # # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)
    #
    #     # Save user_profile
    #     db.session.commit()
    #
    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/portfolio.html')  #, form=form)


@main_blueprint.route('/main/favorites', methods=['GET', 'POST'])
@login_required
def favorites_page():
    # # Initialize form
    # form = UserProfileForm(request.form, obj=current_user)
    #
    # # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)
    #
    #     # Save user_profile
    #     db.session.commit()
    #
    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/favorites.html')  #, form=form)




@main_blueprint.route('/main/trending', methods=['GET', 'POST'])
def trending_page():
    # # Initialize form
    # form = UserProfileForm(request.form, obj=current_user)
    #
    # # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)
    #
    #     # Save user_profile
    #     db.session.commit()
    #
    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/trending.html')  #, form=form)


@main_blueprint.route('/main/specialize', methods=['GET', 'POST'])
@login_required
def specialize_page():
    # # Initialize form
    # form = UserProfileForm(request.form, obj=current_user)
    #
    # # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)
    #
    #     # Save user_profile
    #     db.session.commit()
    #
    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/specialize.html')  #, form=form)


@main_blueprint.route('/main/network', methods=['GET', 'POST'])
@login_required
def network_page():
    # # Initialize form
    # form = UserProfileForm(request.form, obj=current_user)
    #
    # # Process valid POST
    # if request.method == 'POST' and form.validate():
    #     # Copy form fields to user_profile fields
    #     form.populate_obj(current_user)
    #
    #     # Save user_profile
    #     db.session.commit()
    #
    #     # Redirect to home page
    #     return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/network.html')  #, form=form)


@main_blueprint.route('/main/user_settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_portfolio_page'))

    # Process GET or invalid POST
    return render_template('main/user_settings.html', form=form)



# @project_blueprint.route('/project/edit_project', methods=['GET', 'POST'])
@main_blueprint.route('/main/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project_page():
    # Initialize form
    form = ProjectForm(request.form, obj=current_user)
    form.proj_title.data = "Example Project Title"
    form.proj_link.data = "https://www.google.com"
    form.proj_desc.data = "This example description says that clicking the link will send the user to google"

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_portfolio_page'))

    # Process GET or invalid POST
    return render_template('main/edit_project_page.html', form=form)
    # return render_template('main/edit_project_page.html', form=form)
    # return render_template('main/../templates/flask_user/edit_project_page.html', form=form)


@main_blueprint.route('/main/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = NewProjectForm(request.form)
    form.title.data = "Example Project Title"
    form.url.data = "https://www.google.com"
    form.desc.data = "This example description says that clicking the link will send the user to google"

    if form.validate_on_submit():
        # post_new_project()
        # post_new_project(form)
        # return redirect(url_for('success'))
        # return redirect('/main/create_project/post_project', form=form)


        new_project = Project(
            proj_title=request.form['title'],
            proj_desc=request.form['desc'],
            proj_link=request.form['url'],
            user_id=current_user.id
        )
        db.session.add(new_project)
        db.session.commit()

        #Tell user what happened:


        # Redirect to home page
        return redirect(url_for('main.user_portfolio_page'))
        # return redirect('main/create_project=success', form=form)

    return render_template('main/create_project.html', form=form)

@main_blueprint.route('/main/create_project=success', methods=['POST'])
# @main_blueprint.route('/main/create_project/post_project', methods=['POST'])
@login_required
def post_project():

    # # form = NewProjectForm()
    # # if form.validate_on_submit():
    # #     return redirect(url_for('success'))
    # # return render_template('index.html', form=form)
    # project = NewProjectForm(
    #     request.form['title'],
    #     request.form['url'],
    #     request.form['desc']
    # )
    project = NewProjectForm(
        request.form['title'],
        request.form['url'],
        request.form['desc']
    )

    db.session.add(project)
    db.session.commit()

    return redirect('main/portfolio.html')

