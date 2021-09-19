from flask import Blueprint, render_template, session

from library.utilities import services
from library.adapters.repository import repo_instance

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    some_book = services.get_random_books(1, repo_instance)
    # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
    return render_template('home.html',
                           image_url=some_book[0].image_url,
                           bookName=some_book[0].title,
                           releaseYear=some_book[0].release_year,
                           Desc=some_book[0].description,
                           book_id=some_book[0].book_id)


@home_blueprint.route('/user_homepage', methods=['GET'])
def user_homepage():
    if 'user_name' in session:
        user = repo_instance.get_user(session['user_name'])
        number_book = len(user.read_books)
        number_page = 0
        for book in user.read_books:
            if book.num_pages is not None:
                number_page += book.num_pages
        number_read_lower_than_me=0
        for user_temp in repo_instance.get_all_user():
            if len(user_temp.read_books) < number_book:
                number_read_lower_than_me += 1
        percentage = number_read_lower_than_me/len(repo_instance.get_all_user()) *100
        return render_template('user_homepage.html',
                               percentage=percentage,
                               book=number_book,
                               page=number_page)
