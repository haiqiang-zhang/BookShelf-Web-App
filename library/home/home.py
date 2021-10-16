from flask import Blueprint, render_template, session, request

from library.adapters.repository import repo_instance
from library.home import services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    if "user_name" in session:
        user = repo_instance.get_user(session['user_name'])

        rec_book_list = services.get_rec_book(user)

        rec_book = services.get_random_books_by_given_list(rec_book_list)
        if rec_book is None:
            some_book = services.get_random_books(1, repo_instance)
            return render_template('home.html',
                                   image_url=some_book[0].image_url,
                                   bookName=some_book[0].title,
                                   releaseYear=some_book[0].release_year,
                                   Desc=some_book[0].description,
                                   tags=services.print_tags(some_book[0].tags),
                                   book_id=some_book[0].book_id,
                                   authors=some_book[0].authors,
                                   page_title="No Personal Recommendation")

        return render_template('home.html',
                               image_url=rec_book.image_url,
                               bookName=rec_book.title,
                               releaseYear=rec_book.release_year,
                               Desc=rec_book.description,
                               tags=services.print_tags(rec_book.tags),
                               book_id=rec_book.book_id,
                               authors=rec_book.authors,
                               page_title="Personal Recommendation")

    # book = request.args.get("book")
    # book_id = request.args.get("book_id")

    some_book = services.get_random_books(1, repo_instance)

    # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
    # if book_id is not None:
    #     book = repo_instance.get_book(int(book_id))
    #     return render_template('home.html',
    #                        image_url=book.image_url,
    #                        bookName=book.title,
    #                        releaseYear=book.release_year,
    #                        Desc=book.description,
    #                        book_id=book.book_id,
    #                        book=book)

    return render_template('home.html',
                           image_url=some_book[0].image_url,
                           bookName=some_book[0].title,
                           releaseYear=some_book[0].release_year,
                           Desc=some_book[0].description,
                           tags=services.print_tags(some_book[0].tags),
                           book_id=some_book[0].book_id,
                           authors=some_book[0].authors,
                           page_title="Recommendation")
