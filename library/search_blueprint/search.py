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



search_blueprint = Blueprint(
    'search_bp', __name__
)


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        search_content = form.search_content.data
        select_items = form.select.data
        books = []
        try:
            if select_items == "Book ID":
                book = repo_instance.get_book(int(search_content))
                if book is None:
                    raise KeyError
                books.append(book)
            elif select_items == "Book Name":
                books = repo_instance.get_books_by_title(search_content)
                if not books:
                    raise KeyError
            elif select_items == "Author":
                books = repo_instance.get_books_by_authors(search_content)
                if not books:
                    raise KeyError
            else:
                books = repo_instance.get_books_by_release_year(int(search_content))
                if not books:
                    raise KeyError
        except ValueError:
            error = "Invalid Input!"
            return render_template('search.html', handler_url=url_for('search_bp.search'), error=error, form=form)
        except KeyError:
            error = "There are no search results!"
            return render_template('search.html', handler_url=url_for('search_bp.search'), error=error, form=form)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books)
        return render_template('books_list.html', books=books, pages=pages, prev=prev_url, next=next_url, target_page=target_page)
    return render_template('search.html',
                           handler_url=url_for('search_bp.search'),
                           error=error,
                           form=form)


class SearchForm(FlaskForm):
    select = SelectField('Search mode', choices=["Book Name", "Book ID", "Author", "Release Year"])
    search_content = SearchField('Search Content')
    search_submit = SubmitField('')