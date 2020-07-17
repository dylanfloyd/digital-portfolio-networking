# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required, current_app

from app import db
from app.models.user_models import UserProfileForm, User, UsersRoles
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


@main_blueprint.route('/main/user_profile_page', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    if request.method == 'GET':
        projects = current_user.projects
        # print(projects)
        # proj_search_result = Project.query.filter(Project.id == 1).first() #will need to return all projects

    form = request.form
    if request.method =='POST':
        proj_id = form.get('edit_button')
        return render_template('/main/edit_project.html', proj_id=proj_id)

    return render_template('main/user_profile_page.html', current_user=current_user, projects=projects)


@main_blueprint.route('/main/portfolio/<username>', methods=['GET', 'POST'])
@login_required
def portfolio_page(username):

    if request.method == 'GET':
        user = User.query.filter(User.username == username).first()
        projects = user.projects

        # print(projects)
        # proj_search_result = Project.query.filter(Project.id == 1).first() #will need to return all projects

    form = request.form
    if request.method =='POST':
        proj_id = form.get('edit_button')
        return render_template('/main/edit_project.html', proj_id=proj_id)

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
    return render_template('main/portfolio.html', user=user, projects=projects)  #, form=form)


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
        return redirect(url_for('main.user_profile_page'))

    # Process GET or invalid POST
    return render_template('main/user_settings.html', form=form)



# @project_blueprint.route('/project/edit_project', methods=['GET', 'POST'])
@main_blueprint.route('/main/edit_project/<int:proj_id>', methods=['GET', 'POST'])
@login_required
def edit_project_page(proj_id):
    # Initialize form
    #TODO: Remove ex_proj later. Only for demonstration in Milestone 2

    this_project = Project.query.filter(Project.id == proj_id).first() #should only ever be one b/c unique
    this_project_creator_id = this_project.creator_id

    if this_project_creator_id == current_user.id: #Ensures that you can only edit projects if you made it.
        previous_proj_form = EditProjectForm(
            title=this_project.proj_title,
            url=this_project.proj_link,
            desc=this_project.proj_desc,
            tags=this_project.proj_tags
        )


        # Process valid POST
        if request.method == 'POST' and previous_proj_form.validate():
            # Copy form fields to user_profile fields
            # proj_search_result.data = dict(
            #     proj_title=request.form['title'],
            #     proj_desc=request.form['desc'],
            #     proj_link=request.form['url'],
            #     proj_tags=request.form['tags']
            # )
            # form.populate_obj(current_user)

            #Update project in database:
            this_project.proj_title = request.form['title']
            this_project.proj_desc = request.form['desc']
            this_project.proj_link = request.form['url']
            this_project.proj_tags = request.form['tags']


            # Save user_profile
            db.session.commit()

            # Redirect to home page
            return redirect(url_for('main.user_profile_page'))


        # Process GET or invalid POST
        return render_template('main/edit_project_page.html', form=previous_proj_form) #form)

    else:
        current_app.login_manager.unauthorized()
        # current_app.login_manager.unauthorized_callback("You do not have permission to edit this project.")
        return redirect(url_for('main.home_page'))

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
            creator=current_user
        )
        db.session.add(new_project)
        db.session.commit()

        #Tell user what happened:


        # Redirect to home page
        return redirect(url_for('main.user_profile_page'))
        # return redirect('main/create_project=success', form=form)

    return render_template('main/create_project.html', form=form)



# @main_blueprint.route('/main/create_project=success', methods=['POST'])
# # @main_blueprint.route('/main/create_project/post_project', methods=['POST'])
# @login_required
# def post_project():
#
#     # # form = NewProjectForm()
#     # # if form.validate_on_submit():
#     # #     return redirect(url_for('success'))
#     # # return render_template('index.html', form=form)
#     # project = NewProjectForm(
#     #     request.form['title'],
#     #     request.form['url'],
#     #     request.form['desc']
#     # )
#     project = NewProjectForm(
#         request.form['title'],
#         request.form['url'],
#         request.form['desc']
#     )
#
#     db.session.add(project)
#     db.session.commit()
#
#     return redirect('main/portfolio.html')

