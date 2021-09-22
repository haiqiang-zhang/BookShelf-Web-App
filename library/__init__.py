"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template, session

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository
from library.utilities import services
from library.adapters import memory_repository


# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
from library.domain.model import Book



data_path = Path('library') / 'adapters' / 'data'


def create_app(test_config = None):

    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)



    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('library') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    memory_repository.populate(data_path, repo.repo_instance)


    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .book_blueprint import book
        app.register_blueprint(book.book_blueprint)

        from .search_blueprint import search
        app.register_blueprint(search.search_blueprint)

        from .user_homepage_blueprint import user_homepage
        app.register_blueprint(user_homepage.user_homepage_blueprint)

        from .test_blueprint import test
        app.register_blueprint(test.test_blueprint)




    return app