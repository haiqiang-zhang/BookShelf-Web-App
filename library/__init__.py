"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template, session

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository
from library.utilities import services
from library.adapters import memory_repository, repository_populate, database_repository
from library.domain.model import Book
from library.adapters.orm import metadata, map_model_to_tables

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!




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


    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        repository_populate.populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            repository_populate.populate(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()





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