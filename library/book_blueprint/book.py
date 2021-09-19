from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from library.adapters.repository import AbstractRepository
from library.adapters.repository import repo_instance

from library.authentication.authentication import login_required
from library.book_blueprint.services import form_book_list
from better_profanity import profanity
from library.book_blueprint import services


book_blueprint = Blueprint(
    'book_bp', __name__
)


@book_blueprint.route('/books_list')
def books_list():
    session['search_field'] = "All Books"
    books_list = repo_instance.get_all_books()
    target_page = request.args.get('page')
    books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list)
    return render_template(
        'books_list.html',
        list_title="All Books",
        books=books,
        pages=pages,
        prev=prev_url,
        next=next_url,
        target_page=target_page
    )

@book_blueprint.route('/read_book')
@login_required
def read_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_user_read_book(user)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list)
        return render_template(
            'books_list.html',
            list_title="Read Books",
            books=books,
            pages=pages,
            prev=prev_url,
            next=next_url,
            target_page=target_page
        )

@book_blueprint.route('/favourite_book')
@login_required
def favourite_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_favourite(user)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list)
        return render_template(
            'books_list.html',
            list_title="Favourite Books",
            books=books,
            pages=pages,
            prev=prev_url,
            next=next_url,
            target_page=target_page
        )


@book_blueprint.route('/read_a_book')
@login_required
def read_a_book():
    read_book_id = request.args.get("read_book_id")
    user_name = session["user_name"]
    book_instance, user_instance = services.read_a_book_services(repo_instance, user_name, read_book_id)
    if book_instance not in user_instance.read_books:
        user_instance.read_a_book(book_instance)
        return "Succeed!"
    else:
        return "You have read this book!"



@book_blueprint.route('/book_desc')
def book_desc():
    book_id = request.args.get("book_id")
    book = repo_instance.get_book(int(book_id))
    review = book.reviews

    return render_template("book_desc.html",
                           book=book,
                           reviews=review)



@book_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    user_name = session['user_name']
    form = ReviewForm()
    if form.validate_on_submit():
        book_id = int(form.book_id.data)
        services.add_review(book_id, form.review.data, user_name,int(form.rating.data), repo_instance)
        book = repo_instance.get_book(book_id)
        return redirect(url_for('book_bp.book_desc', book_id=book_id))
    if request.method == 'GET':
        book_id = int(request.args.get('book_id'))
        form.book_id.data = book_id
    else:
        book_id = int(form.book_id.data)
    book = repo_instance.get_book(book_id)
    return render_template(
        'Review.html',
        book=book,
        form=form,
        handler_url=url_for('book_bp.review')
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    rating = SelectField('rating', choices=["1", "2", "3", "4", "5"])
    book_id = HiddenField("book id")
    submit = SubmitField('Submit')




