# Week 6 flipped activities (70 mins)

**Make sure you completed the setup in README.md.** This is important as the instructions cover managing environments and dependencies using Poetry which replaces `setup.py` and `venv`.

1. [Create and run a basic Flask app (10 mins)](#activity-1-create-and-run-a-basic-flask-app)
2. [Create a Flask app using the factory pattern (20 mins)](#activity-2-create-a-flask-app-using-the-factory-pattern-approach)
3. [Configure a Flask app (10 mins)](#activity-3-configure-a-flask-app)
4. [Create a Flask app route with an HTML home page that uses Bootstrap CSS (30 mins)](#activity-4-create-a-flask-app-route-with-an-html-home-page-that-uses-bootstrap-css)

## Activity 1: Create and run a basic Flask app

This activity aims to give you 'just enough' knowledge to get a basic Flask webpage that uses both HTML and Bootstrap CSS. It is adapted from '[A minimal application](https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application)' in the Flask documentation.

To complete this activity you will need to have a Python environment in which Flask has been installed (see setup at the start of this document).

### Basic app with a home page

Create a Python file to launch the Flask app. Save it in the `flask_app` folder. Do not call it `flask.py` as this conflicts with Flask itself. `app.py` or the name of your app, e.g. `hello.py` is a more typical name. The rest of this tutorial assumes you have called it `hello.py` so if you name it something else you will need to change the references to suit your filename.

Add the following code section.

`app = Flask(__name__)` creates an instance of the Flask class which is our web app.

`@app.route("/")` is a route decorator that tells Flask when the URL '/' is requested; run the function `def index():`. When the function for the route is called, it will return a page with the HTML paragraph tag with the words 'Hello, World!'.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"
```

To [run a Flask app](https://flask.palletsprojects.com/en/2.2.x/quickstart/) in VS Code, go to Terminal and type

```text
flask --app flask_app/hello --debug run
```

`--app` tells Flask where you app code is. If the app code is in a directory, e.g. in the `flask_app` directory in a module called `hello.py`, then you would type `flask --app flask_app/hello --debug run`.

`--debug` runs the app in debug mode which will enable interactive debugger and the reloader by default which makes errors easier to see and debug.

Some older tutorials will also advise you to set an environment variable e.g. `export FLASK_APP=flask_app/hello` and then type  `flask run`. This is not the method given in the lastest Flask documentation though.

To [run a Flask app in PyCharm Professional](https://flask.palletsprojects.com/en/2.2.x/cli/#pycharm-integration), you should be able to run it using a run configuration. The linked documentation explains how to do this.

You should see the server start. If it successfully starts your Flask app, the URL will be shown in the Terminal. You can open this URL in any browser. By default it will be [http://127.0.0.1:5000](http://127.0.0.1:5000).

If you already have [something running on port 5000](https://flask.palletsprojects.com/en/2.2.x/server/#address-already-in-use), you can change the port in the run options, e.g.

```text
flask --app flask_app/hello --debug run --port 5001
```

You can also start Flask in code which is [explained here](https://flask.palletsprojects.com/en/2.2.x/server/#in-code).

## Activity 2: Create a Flask app using the factory pattern approach

### A reminder on Python packages and modules

[Python package and module](https://realpython.com/python-modules-packages/) is explained in more detail here. There is a folder called `flask_app` in the repository. This folder has a file called `__init__.py` in it which denotes the `flask_app` folder as a Python package. If there were no `__init__.py` then `hello.py` would be a Python module rather than a package. The following shows a basic structure of Flask app as either a module or a package:

A module called `app.py`:

```text
app.py
static/
    mystyles.css
templates/
    hello.html
```

A package called `my_app`:

```text
my_app/
    __init__.py
    app.py
    static/
        mystyles.css
    templates/
        hello.html
```

### Create the app using a factory application function in **init**.py

For all but the smallest projects you are likely to need to separate your code into
[modules and packages](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/#simple-packages).

The [Flask tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/factory/) tells you to create the Flask app object in `__init__.py` using an application factory function. ‘Application factory’ is a design pattern.
This will be necessary later for testing; and also when using Flask extensions/libraries such as Flask-SQLAlchemy for working with the data.

Create a file named `__init__.py` in the `flask_app` folder and add code like the following:

```python
from flask import Flask


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)

    # Include the routes from app.py
    with app.app_context():
        from . import routes

    return app
```

You need to remove the `app = Flask(__name__)` code from `app.py` since the app is now being created in the `create_app()` function instead, e.g.

```python
from flask import Flask

# Delete the following line
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"
```

When you delete the line you are likely to see an error with the index route decorator as `app` is no longer defined.

You need to find a way to reference the app. You can do this using the Flask `current_app` object like this:

```python
from flask import current_app as app

# Remove this and the subsequent line, left in to show what was here before the Factory Application pattern was applied
# app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

```

This still isn't quite enough! Now the routes are aware of the app, however if you try to run the app now you will get an error when you try to access the homepage. The route won't have been created.

Some tutorials place the routes in the `create_app()` function. This is not ideal as you will have a very long function. Instead keep the routes in one place, e.g. in `hello.py`. Some tutorials will suggest that you place the routes in a file named `routes.py` which you can do if you prefer.

To allow the Flask app to find the routes; add the following in `create_app()`. You will need to ignore the unused import warning if you are using a linter.

Application contexts are explained in a later week. If you wish to understand these now then refer to the [Flask documentation on Application contexts](https://flask.palletsprojects.com/en/2.2.x/appcontext/#) or [Patrick Kennedy's explanation of Application and Request contexts](https://www.patricksoftwareblog.com/application-and-request-contexts-in-flask/) (concentrating on Application contexts rather than requests).

```python
from flask import Flask


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)

    # Include the routes from hello.py
    with app.app_context():
        from . import hello

    return app
```

Check you can run the app and go to the home page. To do this you need to modify the run command so it calls the `create_app()` function:

`python -m flask --app 'paralympic_app:create_app()' --debug run`

Note: `--debug` enables the debug mode, when used the flask run command will enable the interactive debugger and the reloader by default, and make errors easier to see and debug.

## Activity 3: Configure a Flask app

Flask uses [configuration parameters](https://flask.palletsprojects.com/en/2.2.x/config/#configuration-handling); some are optional; others will be required for the particular purposes.

One of the config parameters you will need to set is `SECRET_KEY` which is used by Flask and some of the extensions to keep data safe.

For a deployed app, you would not not want to publish this so you would keep it out of GitHub. You are only working in a development or test environment so for ease you can add the secret key to your code.

You can generate random text for a secret key using the python [secrets](https://docs.python.org/3/library/secrets.html) module.

Enter each of the following lines in Terminal in VS Code:

```
python
>> import secrets
>> secrets.token_urlsafe(16)
```

 Copy and paste the resulting ‘key’ into your `create_app()` function after you create the app instance.

 There are different methods to add config parameters, refer to the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/config/#configuration-handling).

 For this activity, modify `create_app` as follows:

```python
def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "add_your_key_here"
```

Check that the app still runs:

`python -m flask --app 'paralympic_app:create_app()' --debug run`

Note: this provides the minimum config needed. You may wish to investigate other ways to configure Flask which are explained in [configuration.md](/activities/configuration.md).

## Activity 4: Create a Flask app route with an HTML home page that uses Bootstrap CSS

### Create the homepage using an HTML template

Flask uses templates to generate pages. The pages can contain HTML and a templating language called [Jinja](https://jinja.palletsprojects.com/en/3.1.x/). We will cover Jinja in a later week.

In this part of the activity, create an HTML-only page template for the homepage.

By default, Flask expects page templates to be in a sub-folder called `templates`.

Create an HTML file called index.html in the templates directory of your Flask app. Add the overall HTML file structure, head and body. In the body add relevant tags with the content 'hello world'.

Refer back to week 1 of the course for the basic structure of an HTML page.

Now, modify the "/" route so that it generates a page using `index.html`. To do this, use the Flask function, [render_template()](https://flask.palletsprojects.com/en/2.2.x/quickstart/#rendering-templates). You also need to add the relevant import.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

To see the change you will need to stop and then restart the Flask app.

In VSCode Press CTRL+C to quit Flask.

Run the app again as you did before in Terminal e.g.

`python -m flask --app 'paralympic_app:create_app()' --debug run`

### Add Bootstrap CSS styling to the homepage

While there are some Flask Bootstrap libraries these don't appear necessarily maintained. So for this part of the course you will use Bootstrap either by downloading their CSS and JavaScript, or using an online hosted version.

The [Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) introduction explains how to either use an online version of Bootstrap, or download and include the files in your project structure.

If you download Bootstrap, you need to place it in the [static](https://flask.palletsprojects.com/en/2.2.x/quickstart/#static-files) folder. Unless you specify otherwise, Flask looks for static files such as CSS and JavaScript in a folder called `static` in a **package**; or in a folder at the same level if you create your Flask app in a **module**.

Bootstrap 5.3 has already been added to the `static` folder for convenience.

Add the Bootstrap CSS to index.html. If you are using a hosted version see [Bootstrap quickstart](https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start) which gives you the HTML to use.

If you are using the version in the static folder, then there is a way to reference the [static file location](https://flask.palletsprojects.com/en/2.2.x/tutorial/static/#static-files) that uses a Jinja syntax and the [Flask `url_for` function](https://flask.palletsprojects.com/en/2.2.x/api/?highlight=url_for#flask.url_for). You will learn about Jinja next week. For now, add the following to the `<head>` section of the html:

```jinja
<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
```

You should now have a simple Flask app that includes the use of HTML and Bootstrap CSS.

## Optional activities

If you want to practice the above activities again, then create a new app called `paralympic_app` and apply  the steps to it. Or if you plan to create a machine learning app, try creating the steps in a new app called `iris_app`.

If you wish to go beyond what you have already learned, try the following activities:

- [Using Blueprints](/activities/blueprints.md)
- [Configuring Flask for different environments](/activities/configuration.md)

There are also many freely available Flask tutorials such as:

- [Flask documentation tutorial](https://flask.palletsprojects.com/en/2.2.x/tutorial/)
- [VS Code Flask tutorial](https://code.visualstudio.com/docs/python/tutorial-flask)
- [PyCharm Flask tutorial](https://www.jetbrains.com/help/pycharm/creating-web-application-with-flask.html)
- [Hackers and Slackers blog](https://hackersandslackers.com/your-first-flask-application/)
- [Patrick Kennedy's blog](https://www.patricksoftwareblog.com/creating-a-simple-flask-web-application/)
- [Miguel Grinberg's 'Flask mega tutorial' blog](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) - this goes well beyond the scope of this first activity!

## Solutions

Potential solutions to all of the activities are in the week 7 starter code.

## Knowledge and skills check

Do you know:

1. Know what a template is in Flask
2. Know what Jinja is and is used for in a Flask app

Can you:

1. Create and run a minimal Flask app
2. Add Bootstrap CSS/JS to an HTML template
3. Configure a Flask app using the Factory Pattern
4. Generate a secret key and add it to the Flask configuration
