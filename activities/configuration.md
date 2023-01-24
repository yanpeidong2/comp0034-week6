# How to configure the Flask app

You may need to refer to the [Flask Configuration documentation](https://flask.palletsprojects.com/en/2.2.x/config/) during this activity.

## Why do you need to care about configuration?

To date we haven't needed to configure the Flask object, however as you start to develop your app you will need to configure the app to work support different functionality, some of which require Flask config parameters.

You will also start to consider working with Flask in different environments. In COMP0035 we considered 3 environments that code may be used in:

- Development environment (dev): where the developer creates the code e.g. your machine
- Testing environment (test): where the testing takes place, this usually mimics the production environment but is likely to have test data and will be configured to provide detailed logging and error reporting. For your coursework this maybe a continuous testing environment that you have configured on GitHub using GitHub Actions.
- Production environment (prod): where the code is deployed and used in the wild. For this coursework you are asked not to deploy the application for ethical reasons (you would need to gain UCL Ethics approval first). If there were no ethics consideration then you could deploy to a free tier of services such as Heroku or AWS.

Complex apps or large organisations may have other environments, however for the purposes of this course the dev, test and prod will be sufficient.

How you configure each environment will vary from a number of perspectives e.g. consider how the database might be different. You may use a SQLite database for development as you have greater control, then you may have a locally hosted Oracle database for testing, and then for production a database that is perhaps split across multiple data centres globally. The location and access details for each of these will be different so you will need to configure Flask differently.

## Where the Flask config values are loaded

Flask provides a `config` attribute for the Flask object that you can use to create a config object to which holds the loaded configuration values. This is the place where Flask itself puts certain configuration values and also where extensions can put their configuration values. But this is also where you can have your own configuration.

## Methods for providing config values

The config attribute is a subclass of a dictionary and can be modified just like any dictionary:

```python
from flask import Flask

app = Flask(__name__)
app.config['TESTING'] = True

# Or provide multiple config parameters using this format
app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/'
)
```

This method becomes unwieldy however when you want to provide different config values for different environments. The methods that can be used include using a config class (`from_object`), using a config file (`from_file`) or from environment variables (`from_envvar`).

```python
from flask import Flask

app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

As you should now be familiar with Python classes then for this course we will focus on creating a config class.

If you intend to create and deploy your own Flask apps after this course however you should investigate the use of environment variables.

We will still use some environment variables within our config class such as 'SECRET_KEY'. In practice leaving this in a config class that is visible to others on GitHub would pose a security risk.

## Create a config class

Create a python file called config.py and create classes within it that reflect the following class diagram:
![Config class diagram](config_class_diag.png)

Your code might look something like this (this is from the Flask documentation):

```python
"""Flask config class."""


class Config(object):
    pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass

```

## Adding the config variables

This section covers some of the variables that you will need for your coursework. There may be others that you
need to add later depending on your application.

Try to add the following to your `config.py`, using appropriate values for each environment.

1. `TESTING = True` to enable testing mode.

You should enable this in your own test environment config. [Flask documentation for TESTING](https://flask.palletsprojects.com/en/2.0.x/config/#TESTING).

2. `SECRET_KEY`

A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application. It should be a long random string of bytes, although unicode is accepted too. For example, copy the output of this to your config:

You can generate a random key in several ways. Try the following to generate a 16 digit key and copy the
resulting text into your `config.py`. You can change the length to any number you wish. Run this in a Python console.

```python
# For python 3.6 and later
import secrets

print(secrets.token_urlsafe(16))
```

Make sure you do not reveal the secret key when posting questions on a public forum or committing code to GitHub!

3. `SQLALCHEMY_DATABASE_URI`,  `SQLALCHEMY_TRACK_MODIFICATIONS`

These are [additional configurationn keys used by the Flask-SQLAlchemy package](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys) which we will use to work with a SQL database.

`SQLALCHEMY_TRACK_MODIFICATIONS = False` needs to be set to avoid warnings. If you want to undersrtand
why [read this stack overflow post](https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196)
.

`SQLALCHEMY_DATABASE_URI` defines the URI that should be used for the connection (i.e. the path to connect to the database).

You are likely to have different databases for different environments. For example, if using an SQL database you might use:

- a local SQLite database for development. These are files and typically use a file extension of .sqlite or .db
- an in memory database for testing (ie one that is created in memory for the tests but not saved to disk)
- a MySQL (or other database server) for production

Example of syntax for these three scenarios:

```python
# A SQLite database in the 'data' directory of the project
import pathlib

basedir = pathlib.Path(__file__).parent.parent
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(basedir.joinpath('data', 'example.sqlite'))

# A SQLite database in the 'data' directory of the project (using 'os' rather than 'pathlib')
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "example.db")

# An in memory SQLite database
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# A MySQL database on a server
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db'
```

You may also want to set `SQLALCHEMY_ECHO = True` for dev and test as this prints database-related actions to console for debugging purposes.

For this activity set the database to the same for all environments and set it to `data/example.sqlite`.

## Apply the config to the Flask create_app function

You will now need to modify the create_app function you created in the previous exercise to pass the config clas name as a parameter e.g.

```python
from flask import Flask


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    # Other code ommited here

    return app
```

You now need to change how you run the app:

`python -m flask --app 'flask_bp:create_app("config.DevelopmentConfig")' --debug run`

## Further examples

- [Flask documentation: Use classes and inheritance for configuration](https://flask.palletsprojects.com/en/2.2.x/config/#development-production)
- [Hackers and slackers: configure Flask applications](https://hackersandslackers.com/configure-flask-applications/)
- [Real Python: Code example in GitHub](https://github.com/realpython/flask-by-example/blob/master/config.py)
