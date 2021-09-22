from typing import List

import pytest

from library.domain.model import Publisher, Author, Book, Review, User, BooksInventory, Tag, make_review
from library.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_book_count(in_memory_repo):
    number_of_books = in_memory_repo.get_number_of_books()

    # Check that the query returned 6 Articles.
    assert number_of_books == 20


def test_repository_can_add_books(in_memory_repo):
    book = Book(
        999999,
        "Test Book"
    )
    in_memory_repo.add_book(book)

    assert in_memory_repo.get_book(999999) is book


def test_repository_can_retrieve_books(in_memory_repo):
    book = in_memory_repo.get_book(25742454)
    assert book.title == "The Switchblade Mamma"
    review_one = [review for review in book.reviews if review.review_text == 'It is a cool book'][0]
    assert review_one.user.user_name == 'zhq'
    assert book.is_tagged_by(Tag('Fantasy')) is False




def test_repository_does_not_retrieve_a_non_existent_book(in_memory_repo):
    article = in_memory_repo.get_book(101)
    assert article is None


def test_repository_can_retrieve_books_by_year(in_memory_repo):
    book = in_memory_repo.get_books_by_release_year(2016)

    # Check that the query returned 3 Articles.
    assert len(book) == 5


def test_repository_does_not_retrieve_an_book_when_there_are_no_book_for_a_given_year(in_memory_repo):
    book = in_memory_repo.get_books_by_release_year(2222)
    assert len(book) == 0


def test_repository_can_retrieve_tags(in_memory_repo):
    tags: List[Tag] = in_memory_repo.get_tags()

    assert len(tags) == 4

    tag_one = [tag for tag in tags if tag.tag_name == 'Action'][0]
    tag_two = [tag for tag in tags if tag.tag_name == 'Adventure'][0]
    tag_three = [tag for tag in tags if tag.tag_name == 'History'][0]
    tag_four = [tag for tag in tags if tag.tag_name == 'Comic'][0]

    assert tag_one.number_of_tagged_books == 4
    assert tag_two.number_of_tagged_books == 4
    assert tag_three.number_of_tagged_books == 3
    assert tag_four.number_of_tagged_books == 17



def test_repository_can_get_books_by_ids(in_memory_repo):
    books = in_memory_repo.get_books_by_id([25742454, 13571772, 11827783])

    assert len(books) == 3
    assert books[0].title == "The Switchblade Mamma"
    assert books[1].title == "Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)"
    assert books[2].title == "Sherlock Holmes: Year One"


def test_repository_does_not_retrieve_books_for_non_existent_id(in_memory_repo):
    book = in_memory_repo.get_books_by_id([25742454, 9])

    assert len(book) == 1
    assert book[0].title == "The Switchblade Mamma"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    book = in_memory_repo.get_books_by_id([0, 9])

    assert len(book) == 0


def test_repository_returns_books_ids_for_existing_tag(in_memory_repo):
    book_ids = in_memory_repo.get_books_ids_for_tag('Action')

    assert (27036536 in book_ids) and (23272155 in book_ids)


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    book_ids = in_memory_repo.get_books_ids_for_tag('United States')

    assert len(book_ids) == 0


def test_repository_can_add_a_tag(in_memory_repo):
    tag = Tag('Literature')
    in_memory_repo.add_tag(tag)

    assert tag in in_memory_repo.get_tags()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(13571772)
    review = make_review("test for book", user, book, 5)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_reivew_without_a_user(in_memory_repo):
    book = in_memory_repo.get_book(27036539)
    review = Review(book, "test for book", 3, None)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_book_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    book = in_memory_repo.get_book(27036539)
    review = Review(None, "test for book", 5, user)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 4
