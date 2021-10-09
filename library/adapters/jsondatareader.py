import json
from typing import List

from library.domain.model import Publisher, Author, Book, Tag
import library.domain.model




class BooksJSONReader:

    def __init__(self, books_file_name: str, authors_file_name: str):
        self.__books_file_name = books_file_name
        self.__authors_file_name = authors_file_name
        self.__dataset_of_books = []

    @property
    def dataset_of_books(self) -> List[Book]:
        return self.__dataset_of_books

    def read_books_file(self) -> list:
        books_json = []
        with open(self.__books_file_name, encoding='UTF-8') as books_jsonfile:
            for line in books_jsonfile:
                book_entry = json.loads(line)
                books_json.append(book_entry)
        return books_json

    def read_authors_file(self) -> list:
        authors_json = []
        with open(self.__authors_file_name, encoding='UTF-8') as authors_jsonfile:
            for line in authors_jsonfile:
                author_entry = json.loads(line)
                authors_json.append(author_entry)
        return authors_json

    def read_json_files(self, repo, data_mode):
        authors_json = self.read_authors_file()
        books_json = self.read_books_file()

        for author_json in authors_json:
            author = Author(int(author_json['author_id']), author_json['name'])
            # if repo.get_author(int(author_json['author_id'])) is None:
            repo.add_author(author)

        for book_json in books_json:
            book_instance = Book(int(book_json['book_id']), book_json['title'])
            if book_json['publisher'] != "":
                publisher_instance = Publisher(book_json['publisher'])
                book_instance.publisher = publisher_instance
                # if book_json['publisher'] not in [publisher_temp.name for publisher_temp in repo.get_publishers()]:
                repo.add_publisher(publisher_instance)
            if book_json['publication_year'] != "":
                book_instance.release_year = int(book_json['publication_year'])
            if book_json['image_url'] != "":
                book_instance.image_url = book_json['image_url']
            if book_json['is_ebook'].lower() == 'false':
                book_instance.ebook = False
            else:
                if book_json['is_ebook'].lower() == 'true':
                    book_instance.ebook = True
            book_instance.description = book_json['description']
            if book_json['num_pages'] != "":
                book_instance.num_pages = int(book_json['num_pages'])

            #add book tag
            for each_element in book_json['popular_shelves']:
                for each_tag in repo.get_tags():
                    if each_tag.tag_name.lower() in each_element["name"].lower():
                        if (book_instance not in each_tag.tagged_books) and (each_tag not in book_instance.tags):
                            each_tag.add_book(book_instance)
                            each_tag.update_size()
                            if data_mode == False:
                                book_instance.tags.append(each_tag)

            # extract the author ids:
            list_of_authors_ids = book_json['authors']
            for author_json in list_of_authors_ids:
                if repo.get_author(int(author_json['author_id'])) is not None:
                    book_instance.add_author(repo.get_author(int(author_json['author_id'])))

            self.__dataset_of_books.append(book_instance)
