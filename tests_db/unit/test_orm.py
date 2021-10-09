import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from library.domain.model import Publisher, Author, Book, User, Review, Tag

def insert_user(empty_session, values=None):
    new_name = "JinhuaTest"
    new_password = "123asd123As"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_Book(empty_session):
    empty_session.execute(
        'INSERT INTO books (book_id, title) VALUES (123321123, "Jinhua And Haiqiang")'
    )
    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def insert_tags(empty_session):
    empty_session.execute(
        'INSERT INTO tags (tag_name, size) VALUES ("Autobiography",0)'
    )
    rows = list(empty_session.execute('SELECT id from tags'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_book_tag_associations(empty_session, book_id, tag_keys):
    stmt = 'INSERT INTO book_tags (book_id, tag_id) VALUES (:book_id, :tag_id)'
    for tag_key in tag_keys:
        empty_session.execute(stmt, {'book_id': book_id, 'tag_id': tag_key})

def insert_reviewed_book(empty_session):
    book_key = insert_Book(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rating = 5

    empty_session.execute(
        'INSERT INTO reviews (user_id, book_id, review_text, rating, timestamp) VALUES '
        '(:user_id, :book_id, "Review 1", :rating, :timestamp_1),'
        '(:user_id, :book_id, "Review 2", :rating, :timestamp_2)',
        {'user_id': user_key, 'rating': rating, 'book_id': book_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT book_id from books').fetchone()
    return row[0]

def make_book():
    return Book(123321123, "Jinhua And Haiqiang")

def make_user():
    return User("Jinhuatest", "123asd123As")

def make_tag():
    return Tag("Autobiography")

def make_Review(review_text, user, book, rating):
    return Review(book, review_text, rating, user)

def test_loading_of_users(empty_session):
    users = list()
    users.append(("jfan200", "1234asdA"))
    users.append(("hzha556", "1111asdA"))
    insert_users(empty_session, users)

    expected = [
        User("jfan200", "1234asdA"),
        User("hzha556", "1111asdA")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("jinhuatest", "123asd123As")]

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("jfan200", "1234asdA"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("jfan200", "1234asdA")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_book(empty_session):
    Book_key = insert_Book(empty_session)
    expected_book = make_book()
    fetched_book = empty_session.query(Book).one()

    assert expected_book == fetched_book

def test_loading_of_tagged_book(empty_session):
    Book_key = insert_Book(empty_session)
    tag_keys = insert_tags(empty_session)
    insert_book_tag_associations(empty_session, Book_key, tag_keys)

    book = empty_session.query(Book).get(Book_key)
    tags = [empty_session.query(Tag).get(key) for key in tag_keys]

    for tag in tags:
        assert book.is_tagged_by(tag)
        assert tag.is_applied_to(book)

def test_loading_of_review_book(empty_session):
    insert_reviewed_book(empty_session)

    rows = empty_session.query(Book).all()
    book = rows[0]

    for review in book.reviews:
        assert review.book is book

def test_saving_of_review(empty_session):
    book_key = insert_Book(empty_session)
    user_key = insert_user(empty_session, ("jfan200", "1234asdA"))

    rows = empty_session.query(Book).all()
    book = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "jfan200").one()

    # Create a new Comment that is bidirectionally linked with the User and Article.
    review_text = "Some comment text."
    review_rating = 5
    review = make_Review(review_text, user, book, review_rating)


    # Note: if the bidirectional links between the new Review and the User and
    # Book objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, book_id, rating, review_text FROM reviews'))

    assert rows == [(user_key, book_key, review_rating, review_text)]

def test_saving_of_book(empty_session):
    article = make_book()
    empty_session.add(article)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT book_id, title FROM books'))

    assert rows == [(123321123, "Jinhua And Haiqiang")]



def test_save_commented_book(empty_session):
    # Create Article User objects.
    book = make_book()
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and Book.
    review_text = "Some comment text."
    review_rating = 5
    make_Review(review_text, user, book, review_rating)

    # Save the new Book.
    empty_session.add(book)
    empty_session.commit()

    # Test test_saving_of_book() checks for insertion into the articles table.
    rows = list(empty_session.execute('SELECT book_id FROM books'))
    book_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the books and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, book_id, rating, review_text FROM reviews'))
    assert rows == [(user_key, book_key, review_rating, review_text)]