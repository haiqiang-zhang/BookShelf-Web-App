import pytest

from library.authentication.services import AuthenticationException
from library.book_blueprint import services as book_services
from library.authentication import services as auth_services
from library.book_blueprint.services import NonExistentArticleException


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    book_id = 13571772
    review_text = 'test review for book'
    user_name = 'fmercury'
    rating = 5

    book_services.add_review(book_id, review_text, user_name, rating, in_memory_repo)


    review_as_list = book_services.get_review(book_id, in_memory_repo)


    assert next(
        (review.review_text for review in review_as_list if review.review_text == review_text),
        None) is not None


def test_cannot_add_reivew_for_non_existent_book(in_memory_repo):
    book_id = 7
    review_text = "for test review"
    user_name = 'fmercury'
    rating = 5


    with pytest.raises(book_services.NonExistentArticleException):
        book_services.add_review(book_id, review_text, user_name,rating, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    book_id = 13571772
    review_text = "for test review"
    user_name = 'gmichael'
    rating = 5

    # Call the service layer to attempt to add the comment.
    with pytest.raises(book_services.UnknownUserException):
        book_services.add_review(book_id, review_text, user_name,rating, in_memory_repo)


def test_can_get_book(in_memory_repo):
    book_id = 13571772

    book = book_services.get_book(book_id, in_memory_repo)

    assert book.book_id == book_id
    assert book.title == 'Captain America: Winter Soldier (The Ultimate Graphic Novels Collection: Publication Order, #7)'
    assert len(book.reviews) == 0

    tag_names = [tag.tag_name for tag in book.tags]
    assert 'Adventure' in tag_names
    assert 'Comic' in tag_names


def test_cannot_get_book_with_non_existent_id(in_memory_repo):
    book_id = 7

    # Call the service layer to attempt to retrieve the Article.
    with pytest.raises(book_services.NonExistentArticleException):
        book_services.get_book(book_id, in_memory_repo)




def test_get_reivews_for_article(in_memory_repo):
    reviews = book_services.get_review(27036539, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(reviews) == 3

    # Check that the comments relate to the article whose id is 1.
    book_ids = [review.book.book_id for review in reviews]
    book_ids = set(book_ids)
    assert 27036539 in book_ids and len(book_ids) == 1


def test_get_reivews_for_non_existent_book(in_memory_repo):
    with pytest.raises(NonExistentArticleException):
        reviews = book_services.get_review(7, in_memory_repo)


def test_get_reivews_for_book_without_reviews(in_memory_repo):
    reviews = book_services.get_review(13571772, in_memory_repo)
    assert len(reviews) == 0

