from flask import Blueprint, render_template, url_for, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from library.adapters.repository import AbstractRepository
from library.adapters.repository import repo_instance
from library.test_blueprint import test

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
    books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.books_list")
    tags = repo_instance.get_tags()

    return render_template(
        'books_list.html',
        list_title="All Books",
        tags=tags,
        books=books,
        pages=pages,
        prev=prev_url,
        next=next_url,
        target_page=target_page,
        url="book_bp.books_list"
    )


@book_blueprint.route('/book_type_list')
def book_type_list():
    session['search_field'] = "All Books"
    books_list = []
    books_list_size = 0
    tag_str = request.args.get('tag')
    for tag in repo_instance.get_tags():
        if tag.tag_name == tag_str:
            books_list = tag.tagged_books
            books_list_size = tag.size
            break
    tags = repo_instance.get_tags()
    total_books = "(Total is " + str(books_list_size) + " books)"
    target_page = request.args.get('page')
    books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.book_type_list", tag_str)

    return render_template(
        'books_list.html',
        list_title=tag_str + " Books",
        total_books=total_books,
        tags=tags,
        books=books,
        pages=pages,
        prev=prev_url,
        next=next_url,
        target_page=target_page,
        tag=tag_str,
        url="book_bp.book_type_list")


@book_blueprint.route('/read_book')
@login_required
def read_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_user_read_book(user)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.read_book")
        return render_template(
            'books_list.html',
            list_title="Read Books",
            books=books,
            pages=pages,
            prev=prev_url,
            next=next_url,
            target_page=target_page,
            url="book_bp.read_book")


@book_blueprint.route('/favourite_book')
@login_required
def favourite_book():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        books_list = repo_instance.get_favourite(user)
        target_page = request.args.get('page')
        books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.favourite_book")
        return render_template(
            'books_list.html',
            list_title="Favourite Books",
            books=books,
            pages=pages,
            prev=prev_url,
            next=next_url,
            target_page=target_page,
            url="book_bp.favourite_book")


@book_blueprint.route('/read_a_book')
@login_required
def read_a_book():
    test.get_test_content(request.referrer)
    read_book_id = request.args.get("read_book_id")
    user_name = session["user_name"]

    #session['search_field'] = "All Books"
    #books_list = repo_instance.get_all_books()
    #target_page = request.args.get('page')
    #books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.books_list")

    book_instance, user_instance = services.read_a_book_services(repo_instance, user_name, read_book_id)
    #tags = repo_instance.get_tags()
    if book_instance not in user_instance.read_books:
        user_instance.read_a_book(book_instance)
        message="Succeed!"
    else:
        message="You have read this book!"
    return message

    # if "books_list" not in request.referrer and "book_type_list" not in request.referrer:
    #     return redirect(url_for('home_bp.home', message=message, book_id=read_book_id))
    # else:
    #     return render_template(
    #         'books_list.html',
    #         message=message,
    #         list_title="All Books",
    #         tags=tags,
    #         books=books,
    #         pages=pages,
    #         prev=prev_url,
    #         next=next_url,
    #         target_page=target_page,
    #         url="book_bp.books_list")


@book_blueprint.route('/favourite_a_book')
@login_required
def favourite_a_book():
    fav_book_id = request.args.get("fav_book_id")
    user_name = session["user_name"]

    session['search_field'] = "All Books"
    #books_list = repo_instance.get_all_books()
    #target_page = request.args.get('page')
    #books, pages, prev_url, next_url, target_page = form_book_list(target_page, books_list, "book_bp.books_list")


    book_instance, user_instance = services.read_a_book_services(repo_instance, user_name, fav_book_id)
    if book_instance not in user_instance.favourite:
        user_instance.favourite.append(book_instance)
        services.auto_add_tag(user_instance, repo_instance)
        message= "Succeed!"
    else:
        message="This book is already your favourite！"

    return message

    # if "books_list" not in request.referrer:
    #     return redirect(url_for('home_bp.home', message=message, book_id=fav_book_id))
    # else:
    #     return render_template(
    #         'books_list.html',
    #         message=message,
    #         list_title="All Books",
    #         books=books,
    #         pages=pages,
    #         prev=prev_url,
    #         next=next_url,
    #         target_page=target_page,
    #         url="book_bp.books_list")



@book_blueprint.route('/book_desc')
def book_desc():
    book_id = request.args.get("book_id")
    review = services.get_review(book_id, repo_instance)
    book = services.get_book(book_id, repo_instance)
    tags_list = []
    tags = repo_instance.get_tags()
    for tag in tags:
        if book in tag.tagged_books and tag.tag_name not in tags_list:
            tags_list.append(tag.tag_name)

    return render_template("book_desc.html",
                           book=book,
                           reviews=review,
                           tags=", ".join(tags_list))


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




@book_blueprint.route('/delete_fav_book')
@login_required
def delete_fav_book():
    try:
        book_id = int(request.args.get("book_id"))
        page = int(request.args.get("page"))
        user_name = session["user_name"]
        services.delete_fav_book_service(book_id, user_name, repo_instance)
        return redirect(url_for("book_bp.favourite_book", page=page))
    except:
        return "Unexpected Error!"


@book_blueprint.route('/delete_read_book')
@login_required
def delete_read_book():
    try:
        book_id = int(request.args.get("book_id"))
        page = int(request.args.get("page"))
        user_name = session["user_name"]
        services.delete_read_book_service(book_id, user_name, repo_instance)
        return redirect(url_for("book_bp.read_book", page=page))
    except:
        return "Unexpected Error!"


