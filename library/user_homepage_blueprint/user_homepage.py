from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms import IntegerField, SubmitField
from library.adapters.repository import repo_instance
from library.authentication.authentication import login_required
from library.user_homepage_blueprint import services
from library.test_blueprint import test

user_homepage_blueprint = Blueprint(
    'user_homepage_bp', __name__)


@user_homepage_blueprint.route('/user_homepage', methods=['GET', 'POST'])
@login_required
def user_homepage():
    user = repo_instance.get_user(session['user_name'])
    number_book = len(user.read_books)
    number_page = 0
    for book in user.read_books:
        if book.num_pages is not None:
            number_page += book.num_pages
    number_read_lower_than_me = 0
    for user_temp in repo_instance.get_all_user():
        if len(user_temp.read_books) < number_book:
            number_read_lower_than_me += 1
    percentage = number_read_lower_than_me / len(repo_instance.get_all_user()) * 100
    form = TagForm()
    form.tag_select.choices = services.get_tag_choice(repo_instance, user)
    if form.validate_on_submit():
        tag = repo_instance.get_tag(form.tag_select.data)
        user.tags.append(tag)
        return redirect(url_for("user_homepage_bp.user_homepage"))

    tags = services.get_tags(user)

    return render_template('user_homepage.html',
                           percentage=round(percentage, 2),
                           book=number_book,
                           page=number_page,
                           tags=tags,
                           form=form,
                           handler_url=url_for("user_homepage_bp.user_homepage"))



@user_homepage_blueprint.route('/delete_tag')
@login_required
def delete_tag():
    tag_name = request.args.get("tag_name")
    tag = repo_instance.get_tag(tag_name)
    user = repo_instance.get_user(session['user_name'])
    user.tags.remove(tag)
    return redirect(url_for("user_homepage_bp.user_homepage"))

class TagForm(FlaskForm):
    tag_select = SelectField('tag_select')
    submit = SubmitField('Add Tag')
