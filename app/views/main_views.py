# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template, flash
from flask import request, url_for
from flask_user import current_user, login_required, roles_required, current_app

from app import db
from app.models.user_models import UserProfileForm, User, UsersRoles
from app.models.project_models import EditProjectForm, NewProjectForm, Project, ProjectLike, ProjectSearchForm
from sqlalchemy import or_, desc, asc
import re
# import flask_whooshalchemy as wa

main_blueprint = Blueprint('main', __name__, template_folder='templates')
# wa.whoosh_index(app=current_app, model=Project)
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

    # Initialize form
    form = request.form

    # Process valid POST
    if request.method =='POST':
        proj_id = form.get('edit_button')
        return render_template('/main/edit_project.html', proj_id=proj_id)



    # Process GET or invalid POST
    return render_template('main/portfolio.html', current_user=current_user, user=user, projects=projects)  #, form=form)


@main_blueprint.route('/main/favorites', methods=['GET', 'POST'])
@login_required
def favorites_page():
    #TODO: Must be a more efficient way to query at scale and get projs and avoid for loop.
    projects = Project.query.order_by(desc(Project.date_added)).all()
    # fav_projects = Project.query.filter(ProjectLike.user_id == current_user.id).all()
    fav_projects = []
    for proj in projects:
        if current_user.has_liked_project(proj):
            fav_projects.append(proj)


    return render_template('main/favorites.html', current_user=current_user, projects=fav_projects)  #, form=form)




@main_blueprint.route('/main/trending', methods=['GET', 'POST'])
def trending_page():
    ##TODO: Add an if statement to check if anyone is logged in or not. Need a new render card for user not logged in.
    projects = Project.query.all()

    return render_template('main/trending.html', current_user=current_user, projects=projects)  #, form=form)


@main_blueprint.route('/main/specialize', methods=['GET', 'POST'])
@login_required
def specialize_page():
    interests_str = current_user.interests.lower()
    rgx = r'#[a-zA-Z]+'
    all_interests = re.findall(rgx, interests_str)
    all_interests_set = set(all_interests)
    relevant_projects = []
    relevant_tags = []
    all_projects = Project.query.all() #.order_by(Project.date_added.desc())
    for proj in all_projects:
        ptags_str = proj.proj_tags.lower()
        ptags = re.findall(rgx, ptags_str)
        these_relevant_tags = all_interests_set.intersection(ptags)
        if len(these_relevant_tags) > 0:
            relevant_tags.extend(list(these_relevant_tags))
            relevant_projects.append(proj)

    relevant_tags = list(set(relevant_tags).intersection(relevant_tags)) #removes duplicate tags
    #TODO: improve specialization results by adding less relevant results after exact matches
    #Can add another option to check for similar substrings, and put those projects after the more relevant ones.
    #Example: #learning could return #machinelearning, but it'd be less relevant b/c not explicitly stated



    return render_template('main/specialize.html', current_user=current_user, projects=relevant_projects, tags_matched=relevant_tags)  #, form=form)


@main_blueprint.route('/main/network', methods=['GET', 'POST'])
@login_required
def network_page():

    projects_from_network = current_user.followed_projects()


    return render_template('main/network.html', current_user=current_user, projects=projects_from_network)  #, form=form)

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
        # return redirect(request.referrer.referrer)

    #TODO:  invalid POST

    # Process GET
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
            tags=this_project.proj_tags,
            privacy=this_project.privacy_setting
        )


        # Process valid POST
        if request.method == 'POST' and previous_proj_form.validate():
            # post_form = EditProjectForm(request.form)
            # assert False==True
            # if post_form.validate_on_submit():
            #     if post_form.delete.data:
            #         worked=True
            #         assert False == True
            #
            # # if post_form.delete.data:
            #     kinda=True
            #     assert False == True
            #
            # not_even_close=True
            # assert False==True

            #Update project in database:
            this_project.proj_title = request.form['title']
            this_project.proj_desc = request.form['desc']
            this_project.proj_link = request.form['url']
            this_project.proj_tags = request.form['tags']
            this_project.privacy_setting = request.form['privacy']

            # Save user_profile
            db.session.commit()


            # Redirect to home page
            return redirect(url_for('main.user_profile_page'))


        # Process GET or invalid POST
        return render_template('main/edit_project_page.html', form=previous_proj_form, proj_id=proj_id, project=this_project) #form)

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
            privacy_setting=request.form['privacy'],
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

@main_blueprint.route('/favorite/<int:project_id>/<action>')
@login_required
def favorite_action(project_id, action):
    project = Project.query.filter_by(id=project_id).first_or_404()
    if action == 'favorite':
        current_user.like_project(project)
        db.session.commit()
    if action == 'unfavorite':
        current_user.unlike_project(project)
        db.session.commit()
    return redirect(request.referrer)

@main_blueprint.route('/follow/<int:user_id>/<action>')
@login_required
def follow_action(user_id, action):
    some_user = User.query.filter_by(id=user_id).first_or_404()
    if action == 'follow':
        current_user.follow_user(some_user)
        db.session.commit()
    if action == 'unfollow':
        current_user.unfollow_user(some_user)
        db.session.commit()
    return redirect(request.referrer)

@main_blueprint.route('/main/search_page/results')
def search(search_form):
    results = []
    search_str = search_form.data['searchbar']

    if search_str == '':
        results = Project.query.all()
    else:
        words = search_str.split(' ')
        for word in words:
            search_input = "%{0}%".format(word)
            word_relevant_projects = Project.query.filter(or_(Project.proj_title.like(search_input),
                                                Project.proj_desc.like(search_input),
                                                Project.proj_tags.like(search_input),
                                                User.username == search_input[1:-1],
                                                User.first_name == search_input[1:-1],
                                                User.last_name == search_input[1:-1])).distinct().all()
            # for wrp in word_relevant_projects:
            #     if wrp not in results:
            #         results.append(wrp)
            results.extend(word_relevant_projects)

    if len(results) == 0:
        flash('No results found. Please try searching for another term.')
        return redirect(url_for('main.search_page'))
    else:
        final_results = list(set(results).intersection(results))
        return render_template('main/search_page.html', form=search_form, projects=final_results, current_user=current_user)


@main_blueprint.route('/main/search_page', methods=['GET', 'POST'])
def search_page():
    search_form = ProjectSearchForm(request.form)
    if search_form.validate_on_submit():
    # if request.method == 'POST':
        return search(search_form)
    projects = []
    return render_template('main/search_page.html', form=search_form, projects=projects, current_user=current_user)  #, form=form)




@main_blueprint.route('/main/delete_project/<int:proj_id>', methods=['GET'])
@login_required
def delete_project_page(proj_id):
    # Initialize form
    #TODO: Remove ex_proj later. Only for demonstration in Milestone 2

    this_project = Project.query.filter(Project.id == proj_id).first() #should only ever be one b/c unique
    this_project_creator_id = this_project.creator_id

    if this_project_creator_id == current_user.id: #Ensures that you can only edit projects if you made it.
        Project.query.filter_by(id=proj_id).delete()
        db.session.commit()
        return redirect(url_for('main.user_profile_page'))

    else:
        current_app.login_manager.unauthorized()
        # current_app.login_manager.unauthorized_callback("You do not have permission to edit this project.")
        return redirect(url_for('main.home_page'))
