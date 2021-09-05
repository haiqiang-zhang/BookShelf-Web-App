from flask import Blueprint, render_template

from library.utilities import services
from library.adapters.repository import repo_instance

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    some_book = services.get_random_books(1, repo_instance)
    # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
    return render_template('home.html',
                           bookName=some_book[0].title,
                           releaseYear=some_book[0].release_year,
                           Desc=some_book[0].description)
