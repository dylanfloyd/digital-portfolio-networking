# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm
from app.models.project_models import EditProjectForm, NewProjectForm, Project
# from forms import NewProjectForm

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
    if request.method == 'GET':
        proj_search_result = Project.query.filter(Project.id == 1).first()
        result_title = proj_search_result.proj_title


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
    return render_template('main/portfolio.html', value=result_title)  #, form=form)


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
    #TODO: Remove ex_proj later. Only for demonstration in Milestone 2

    proj_search_result = Project.query.filter(Project.id == 1).first()
    # print(proj_search_result)
    # print("proj_search_result found!!!")
    previous_proj_form = EditProjectForm(
        title=proj_search_result.proj_title,
        url=proj_search_result.proj_link,
        desc=proj_search_result.proj_desc,
        tags=proj_search_result.proj_tags
    )

    # ex_proj = Project.query.filter(Project.id==1).first()
    # form = EditProjectForm(request.form)
    # form.title = ex_proj.proj_title
    # form.url = ex_proj.proj_link
    # form.desc = ex_proj.proj_desc
    # form.tags = ex_proj.proj_tags

    # form.proj_title = "Example Project Title"
    # form.proj_link = "https://www.google.com"
    # form.proj_desc = "This example description says that clicking the link will send the user to google"
    # form.proj_tags = "#These #Are #Some #Example #ProjectTags #That #Can #B #Used #To #HelpUsersFindYourWork"

    # Process valid POST
    if request.method == 'POST' and previous_proj_form.validate():
        # Copy form fields to user_profile fields
        proj_search_result.data = dict(
            proj_title=request.form['title'],
            proj_desc=request.form['desc'],
            proj_link=request.form['url'],
            proj_tags=request.form['tags']
        )
        # form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.user_portfolio_page'))

    # else:
    #     form = EditProjectForm(request.form)
    #     # form.title = ex_proj.proj_title
    #     # form.url = ex_proj.proj_link
    #     # form.desc = ex_proj.proj_desc
    #     # form.tags = ex_proj.proj_tags
    #     form.proj_title = "Example Project Title"
    #     form.proj_link = "https://www.google.com"
    #     form.proj_desc = "This example description says that clicking the link will send the user to google"
    #     form.proj_tags = "#These #Are #Some #Example #ProjectTags #That #Can #B #Used #To #HelpUsersFindYourWork"
    #     db.session.commit()

    # Process GET or invalid POST
    return render_template('main/edit_project_page.html', form=previous_proj_form) #form)
    # return render_template('main/edit_project_page.html', form=form)
    # return render_template('main/../templates/flask_user/edit_project_page.html', form=form)


@main_blueprint.route('/main/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = NewProjectForm(request.form)
    form.title.data = "Example Project Title"
    form.url.data = "https://www.google.com"
    form.desc.data = "This example description says that clicking the link will send the user to google"
    form.tags.data = "#Project #Tags"

    if form.validate_on_submit():
        # post_new_project()
        # post_new_project(form)
        # return redirect(url_for('success'))
        # return redirect('/main/create_project/post_project', form=form)


        new_project = Project(
            proj_title=request.form['title'],
            proj_desc=request.form['desc'],
            proj_link=request.form['url'],
            proj_tags=request.form['tags'],
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

