from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from library.domain import model

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
    # Column('pages_read', Integer)
)

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id')),
    Column('review_text', String(1024), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

books_table = Table(
    'books', metadata,
    Column('book_id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('release_year', Integer),
    Column('image_url', String(255)),
    # Column('rating', Integer),
    Column('num_pages', Integer),
    # Column('rating_count', Integer),
    Column('publisher_id', Integer, ForeignKey('publishers.publisher_id'))
)

tags_table = Table(
    'tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('tag_name', String(64), nullable=False),
    Column('size', Integer, nullable=False)
)

books_tags_table = Table(
    'book_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('tag_id', ForeignKey('tags.id'))
)

authors_table = Table(
    'authors', metadata,
    Column('author_id', Integer, primary_key=True),
    Column('full_name', String(255), nullable=False)
)

books_authors_table = Table(
    'book_authors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('book_id', ForeignKey('books.book_id')),
    Column('author_id', ForeignKey('authors.author_id'))
)

users_tags_table = Table(
    'user_tags', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('tag_id', ForeignKey('tags.id'))
)

read_list_table = Table(
    'read_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id'))
)

favourite_list_table = Table(
    'favourite_list', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.book_id'))
)

publishers_table = Table(
    'publishers', metadata,
    Column('publisher_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)




def map_model_to_tables():
    mapper(model.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        # '_User__pages_read': users_table.c.pages_read,
        '_User__reviews': relationship(model.Review, backref='_Review__user'),
        '_User__read_books': relationship(
            model.Book,
            secondary=read_list_table,
            back_populates="_Book__read_list_user"
        ),
        '_User__favourite': relationship(
            model.Book,
            secondary=favourite_list_table,
            back_populates="_Book__favourite_list_user"
        ),
        '_User__tags': relationship(
            model.Tag,
            secondary=users_tags_table,
            back_populates="_Tag__user"
        )
    })
    mapper(model.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.review_text,
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__rating': reviews_table.c.rating
    })

    mapper(model.Publisher, publishers_table, properties={
        '_Publisher__name': publishers_table.c.name,
        '_Publisher__books': relationship(model.Book, backref='_Book__publisher')
    })

    mapper(model.Book, books_table, properties={
        '_Book__book_id': books_table.c.book_id,
        '_Book__title': books_table.c.title,
        '_Book__description': books_table.c.description,
        '_Book__release_year': books_table.c.release_year,
        '_Book__image_url': books_table.c.image_url,
        # '_Book__rating': books_table.c.rating,
        # '_Book__rating_count': books_table.c.rating_count,
        '_Book__num_pages': books_table.c.num_pages,
        '_Book__reviews': relationship(model.Review, backref='_Review__book'),
        '_Book__tags': relationship(model.Tag, secondary=books_tags_table, back_populates='_Tag__tagged_books'),
        '_Book__authors': relationship(
            model.Author,
            secondary=books_authors_table,
            back_populates="_Author__author_books"
        ),
        '_Book__read_list_user': relationship(
            model.User,
            secondary=read_list_table,
            back_populates="_User__read_books"
        ),
        '_Book__favourite_list_user': relationship(
            model.User,
            secondary=favourite_list_table,
            back_populates="_User__favourite"
        )
    })

    mapper(model.Tag, tags_table, properties={
        '_Tag__tag_name': tags_table.c.tag_name,
        '_Tag__tagged_books': relationship(
            model.Book,
            secondary=books_tags_table,
            back_populates="_Book__tags"
        ),
        '_Tag__size': tags_table.c.size,
        '_Tag__user': relationship(
            model.User,
            secondary=users_tags_table,
            back_populates="_User__tags"
        )
    })

    mapper(model.Author, authors_table, properties={
        '_Author__unique_id': authors_table.c.author_id,
        '_Author__full_name': authors_table.c.full_name,
        '_Author__author_books': relationship(
            model.Book,
            secondary=books_authors_table,
            back_populates="_Book__authors"
        )
    })


