from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from library.domain.model import *
from library.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_all_user(self) -> List[User]:
        return self._session_cm.session.query(User).all()

    def get_user_num_of_read_book(self, user: User) -> int:
        return len(user.read_books)

    def get_user_read_book(self, user: User) -> List[Book]:
        return user.read_books

    def get_favourite(self, user: User):
        return user.favourite

    def add_book(self, book: Book):
        with self._session_cm as scm:
            scm.session.add(book)
            scm.commit()


    def get_book(self, id: int) -> Book:
        book = None
        try:
            book = self._session_cm.session.query(Book).filter(Book._Book__book_id == id).one()
        except NoResultFound:
            pass
        return book

    def get_all_books(self) -> List[Book]:
        return self._session_cm.session.query(Book).all()

    def get_books_by_release_year(self, release_year: int) -> List[Book]:
        matching_articles = self._session_cm.session.query(Book).filter(Book._Book__release_year == release_year).all()

        return matching_articles

    def get_number_of_books(self) -> int:
        return self._session_cm.session.query(Book).count()

    def get_books_by_index(self, index: List[int]) -> List[Book]:
        return [self._session_cm.session.query(Book).all()[index] for index in index]

    def get_books_by_authors(self, author_input: str) -> List[Book]:
        author_input = author_input.lower()
        matching_articles = self._session_cm.session.query(Book)\
            .filter(Book._Book__authors.match("%{}%".format(author_input))).all()

        return matching_articles

    def get_books_by_publisher(self, publisher: Publisher) -> List[Book]:
        matching_articles = list()
        try:
            matching_articles = publisher.books
        except KeyError:
            pass
        return matching_articles

    def get_books_by_title(self, title: str) -> List[Book]:
        title = title.lower()
        matching_articles = self._session_cm.session.query(Book) \
            .filter(Book._Book__title.match("%{}%".format(title))).all()

        return matching_articles

    def get_tag(self, tag_name):
        tag = None
        try:
            tag = self._session_cm.session.query(Tag).filter(Tag._Tag__tag_name == tag_name).one()
        except NoResultFound:
            pass
        return tag

    def get_books_ids_for_tag(self, tag_name: str):
        # Linear search_blueprint, to find the first occurrence of a Tag with the name tag_name.
        tag: Tag = self.get_tag(tag_name)

        # Retrieve the ids of articles associated with the Tag.
        if tag is not None:
            book_ids = [book.book_id for book in tag.tagged_books]
        else:
            # No Tag with name tag_name, so return an empty list.
            book_ids = list()
        return book_ids

    def add_tag(self, tag: Tag):
        with self._session_cm as scm:
            scm.session.add(tag)
            scm.commit()

    def get_tags(self):
        return self._session_cm.session.query(Tag).all()


    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self):
        return self._session_cm.session.query(Review).all()

    def add_publisher(self, publisher:Publisher):
        with self._session_cm as scm:
            scm.session.add(publisher)
            scm.commit()

    def get_publishers(self):
        return self._session_cm.session.query(Publisher).all()


    def add_author(self, author:Author):
        with self._session_cm as scm:
            scm.session.add(author)
            scm.commit()

    def get_authors(self):
        return self._session_cm.session.query(Author).all()


    def get_author(self, id: int):
        author = None
        try:
            author = self._session_cm.session.query(Author).filter(Author._Author__unique_id == id).one()
        except NoResultFound:
            pass
        return author

