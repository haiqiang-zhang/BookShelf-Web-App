from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms import IntegerField, SubmitField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Length, ValidationError
from library.adapters.repository import AbstractRepository
from library.adapters.repository import repo_instance
from library.authentication.authentication import login_required
from library.book_blueprint.services import form_book_list
from library.search_blueprint.services import get_search_books, search_book
from library.test_blueprint import test

research_book_result = []
search_scope = []
scope_text = ""

search_blueprint = Blueprint(
    'search_bp', __name__
)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    global research_book_result, search_scope, scope_text
    research_book_result = []
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        search_content = form.search_content.data
        select_items = form.select.data
        try:
            research_book_result = search_book(repo_instance, select_items, search_content, search_scope).copy()
        except ValueError:
            error = "Invalid Input!"
            return render_template('search.html', handler_url=url_for('search_bp.search'), error=error, form=form,
                                   scope_text=scope_text)
        except KeyError:
            error = "There are no search results!"
            return render_template('search.html', handler_url=url_for('search_bp.search'), error=error, form=form,
                                   scope_text=scope_text)
        return redirect(url_for("search_bp.search_result", page=1))
    search_scope = []
    scope_text = ""
    search_scope, scope_text = get_search_books(request.referrer, repo_instance)
    test.test_content = search_scope
    return render_template('search.html',
                           handler_url=url_for('search_bp.search'),
                           error=error,
                           form=form,
                           scope_text=scope_text)


class SearchForm(FlaskForm):
    select = SelectField('Search mode', choices=["Book Name", "Book ID", "Author", "Release Year"])
    search_content = SearchField('Search Content')
    search_submit = SubmitField('')


@search_blueprint.route('/search_result')
def search_result():
    global research_book_result
    target_page = request.args.get("page")
    books, pages, prev_url, next_url, target_page = form_book_list(target_page, research_book_result, "Search Result")
    return render_template('books_list.html', books=books, pages=pages, prev=prev_url, next=next_url,
                           target_page=target_page, list_title="Search Result", scope_text=scope_text)
