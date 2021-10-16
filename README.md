# "Bookshelf" Web App (DB Edition)
### Team: NJUST Team1
### Author: Haiqiang Zhang & Jinhua Fan

---


## Description

We design the "BookShelf" Web App to show books information, manage user's reading data, and provide personal recommendations to specific users. We hope it will develop into the best **digital reading management tool!**

User can use the web app to realize the entire process of reading management: choosing book →  manage favourite book list → add book to read list → compare with other user to stimulate the reading passion → review books.

We will continuous develop the web app in the future.

l will introduce the features of each unit separately in _**Report.pdf**_.

Now the web app support database by SQLite.

## Website
I have deployed the web app to a server. You can access the website directly to have fun.
The Website is: http://165.232.174.128:5000/


## Python version

Please use Python version 3.6 or newer versions for development. Some of the depending libraries of our web application do not support Python versions below 3.6!


## Installation

**Installation via requirements.txt**

### Linux
```shell
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```
### MacOS
```shell
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```
### Windows
```shell
$ python3 -m venv venv
$ \venv\bin\activate
$ pip install -r requirements.txt
```

When using PyCharm for requirements installation, set the virtual environment using 'File'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Configuration

The *compsci235-assignment2-njust-team1/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

These settings are for the database version of the code:

* `SQLALCHEMY_DATABASE_URI`: The URI of the SQlite database, by default it will be created in the root directory of the project.
* `SQLALCHEMY_ECHO`: If this flag is set to True, SQLAlchemy will print the SQL statements it uses internally to interact with the tables. 
* `REPOSITORY`: This flag allows us to easily switch between using the Memory repository or the SQLAlchemyDatabase repository.

## Execution of the web application

**Running the Flask application**

From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

**Externally Visible Server**

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding `--host=0.0.0.0` to the command line:
```shell
$ flask run --host=0.0.0.0
```


## Testing with the pytest unit tests

```shell
$ python -m pytest -v tests
$ python -m pytest -v tests_db
```

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Test with showing the variable content
I use the test_blueprint to debug. It can show specific variables' content to debug.

The content will be shown in [http://127.0.0.1:5000/test](http://127.0.0.1:5000/test)

We can call `get_test_content(content)` to transfer parameters


## Data sources 

The data in the excerpt files were downloaded from (Comic & Graphic):
https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

On this webpage, you can find more books and authors in the same file format as in our excerpt, for example for different book genres. 
These might be useful to extend your web application with more functionality.

We would like to acknowledge the authors of these papers for collecting the datasets by extracting them from Goodreads:

*Mengting Wan, Julian McAuley, "Item Recommendation on Monotonic Behavior Chains", in RecSys'18.*

*Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, "Fine-Grained Spoiler Detection from Large-Scale Review Corpora", in ACL'19.*
