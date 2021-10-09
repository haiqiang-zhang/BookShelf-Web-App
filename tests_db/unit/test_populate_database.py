from sqlalchemy import select, inspect

from library.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'book_tags', 'books', 'favourite_list', 'publishers', 'read_list',  'reviews', 'tags', 'user_tags', 'users']

def test_database_populate_select_all_authors(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tags_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_tags_table]])
        result = connection.execute(select_statement)


        all_authors = []
        for row in result:
            all_authors.append((row["author_id"], row["book_id"]))

        assert len(all_authors) == 35

def test_database_populate_select_all_tags(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tags_table = inspector.get_table_names()[8]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_tags_table]])
        result = connection.execute(select_statement)


        all_tag_names = []
        for row in result:
            all_tag_names.append(row["tag_name"])

        assert len(all_tag_names) == 4

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[10]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert len(all_users) == 5

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_comments_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table comments
        select_statement = select([metadata.tables[name_of_comments_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['book_id'], row['review_text']))

        assert len(all_comments) == 4

def test_database_populate_select_all_books(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_articles_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_articles_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            print(row)
            all_books.append((row['book_id'], row['title']))

        nr_articles = len(all_books)
        assert nr_articles == 20

        assert all_books[0] == (707611, 'Superman Archives, Vol. 2')

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tags_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tags
        select_statement = select([metadata.tables[name_of_tags_table]])
        result = connection.execute(select_statement)


        all_publishers = []
        for row in result:
            all_publishers.append(row["name"])

        assert len(all_publishers) == 15

