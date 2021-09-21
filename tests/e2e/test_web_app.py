import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Bookshelf' in response.data


def test_login_required_to_comment(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the comment page.
    response = client.get('/review?book_id=707611')

    response = client.post(
        '/review',
        data={'review': 'Who needs quarantine?', 'book_id': 707611, 'rating': '5'}
    )
    assert response.headers['Location'] == 'http://localhost/book_desc?book_id=707611'


@pytest.mark.parametrize(('review_text', 'messages'), (
        ('Who thinks Trump is a f***wit?', (b'Your comment must not contain profanity')),
        ('Hey', (b'Your comment is too short')),
        ('ass', (b'Your comment is too short', b'Your comment must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review_text, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article.
    response = client.post(
        '/review',
        data={'review': review_text, 'book_id': 707611, 'rating': '5'}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_book_with_tag(client):
    # Check that we can retrieve the articles page.
    response = client.get('/book_type_list?tag=Action')
    assert response.status_code == 200

    # Check that without providing a date query parameter the page includes the first article.
    assert b'Bookshelf' in response.data
    assert b'Action Books (Total is 4 books)' in response.data


def test_read_book(client,auth):
    # Check that we can retrieve the articles page.
    auth.login()
    response = client.get('/read_book')
    assert response.status_code == 200

    # Check that all articles on the requested date are included on the page.
    assert b'Read Books' in response.data


def test_search_book(client):


    response = client.post(
        '/search',
        data={'select': "Release Year", 'search_content': "2016"}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/search_result?page=1'


def test_show_tags(client):
    # Check that we can retrieve the articles page.
    response = client.get('/books_list')
    assert response.status_code == 200

    # Check that all articles tagged with 'Health' are included on the page.
    assert b'Action' in response.data
    assert b'Adventure' in response.data
