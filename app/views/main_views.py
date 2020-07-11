# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm

main_blueprint = Blueprint('main', __name__, template_folder='templates')
flask_user_blueprint = Blueprint('flask_user', __name__, template_folder='templates')

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




@main_blueprint.route('/main/edit_project', methods=['GET', 'POST'])
@login_required
def edit_project_page():
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
    return render_template('main/edit_project.html', form=form)