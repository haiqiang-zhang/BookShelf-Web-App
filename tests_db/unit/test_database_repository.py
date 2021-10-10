from datetime import date, datetime

import pytest

import library.adapters.repository as repo
from library.adapters.database_repository import SqlAlchemyRepository
from library.domain.model import Publisher, Author, Book, User, Review, Tag
from library.adapters.repository import RepositoryException


#Test User
def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('abc123', '123456789')
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('abc123')

    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('jinhua')
    assert user == User('jinhua', '123asd12A')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None



#Test Book
def test_repository_can_retrieve_user_read_book_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user =User('jinhua', '123asd12A')

    number_of_book = repo.get_user_num_of_read_book(user)

    # Check that the query returned 0 books.
    assert number_of_book == 0

def test_repository_can_get_user_read_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user =User('jinhua', '123asd12A')

    books = repo.get_user_read_book(user)


    assert books == []

def test_repository_can_get_favourite(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('jinhua', '123asd12A')

    favourite = repo.get_favourite(user)

    # Check that the Article has the expected title.
    assert favourite == []

def test_repository_can_add_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, "Test Book")

    repo.add_book(book)

    book1 = repo.get_book(123456)

    assert book1 == book

def test_repository_can_get_book(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = Book(123456, "Test Book")

    repo.add_book(book)

    book1 = repo.get_book(123456)

    assert book1 == book

def test_repository_can_get_all_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_all_books()

    assert books != []

def test_repository_can_get_books_by_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_release_year(2006)

    books_list = []

    books_list.append(Book(2168737, "The Thing: Idol of Millions"))
    books_list.append(Book(13340336, "20th Century Boys, Libro 15: ¡Viva la Expo! (20th Century Boys, #15)"))

    assert books == books_list

def test_repository_can_get_number_of_books(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    num = repo.get_number_of_books()

    assert num == 47

def test_repository_can_get_books_by_index(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_index([1, 5])

    books_list = []

    books_list.append(Book(250810, "Inherit the Wind"))
    books_list.append(Book(598195, "Borderlands/La Frontera"))

    assert books == books_list

def test_repository_can_get_books_by_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_authors("Yuu Asami")
    assert len(books) == 1

def test_repository_can_get_books_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    publisher = Publisher("jinhua")
    books = repo.get_books_by_publisher(publisher)

    assert books == []

def test_repository_can_get_books_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_by_title("Inherit the Wind")

    assert books == [Book(250810, "Inherit the Wind")]



#Test Tag
def test_repository_can_retrieve_tags(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tags = repo.get_tags()

    assert len(tags) == 12

    tag_one = [tag for tag in tags if tag.tag_name == 'Action'][0]
    tag_two = [tag for tag in tags if tag.tag_name == 'Adventure'][0]


    assert tag_one.size == 4
    assert tag_two.size == 5

def test_repository_can_get_books_ids_for_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    books = repo.get_books_ids_for_tag("Action")

    assert books == [27036536, 23272155, 11827783, 18955715]

def test_repository_can_add_tag(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tag = Tag("Acg")
    repo.add_tag(tag)

    tags = repo.get_tags()

    assert len(tags) == 13




#Test review
def test_repository_can_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(250810)
    user = repo.get_user("jinhua")
    review = Review(book, "Great book!", 5, user)
    repo.add_review(review)

    assert review in repo.get_reviews()

def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    book = repo.get_book(250810)
    review = Review(book, "Great book!", 5, None)

    with pytest.raises(RepositoryException):
        repo.add_review(review)

def test_repository_can_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    reviews = repo.get_reviews()

    assert len(reviews) != 0




#Test Publisher
def test_repository_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    size1 = len(repo.get_publishers())

    publisher = Publisher("jinhua")
    repo.add_publisher(publisher)

    size2 = len(repo.get_publishers())

    assert size1 != size2




#Test Author
def test_repository_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    size1 = len(repo.get_authors())

    author = Author(123456, "jinhua")
    repo.add_author(author)
    size2 = len(repo.get_authors())

    author1 = repo.get_author(123456)


    assert author1 == author
    assert size1 != size2