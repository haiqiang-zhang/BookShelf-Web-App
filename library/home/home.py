from flask import Blueprint, render_template, session,request

from library.adapters.repository import repo_instance
from library.utilities import services

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    message = request.args.get("message")
    #book_id = request.args.get("book_id")

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
    #                        message=message)

    return render_template('home.html',
                           image_url=some_book[0].image_url,
                           bookName=some_book[0].title,
                           releaseYear=some_book[0].release_year,
                           Desc=some_book[0].description,
                           book_id=some_book[0].book_id,
                           message=message)


