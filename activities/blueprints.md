# Apply a Blueprint to a Flask app

This activity covers another pattern used in Flask apps, [Blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/)

## What is a Blueprint?

> "Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register operations on applications. A Blueprint object works similarly to a Flask application object, but it is not actually an application. Rather it is a blueprint of how to construct or extend an application."

A Flask blueprint is a way to organize a flask application into smaller and re-usable components.

A blueprint defines a collection of views, templates and static assets.

If you write your blueprint in a separate Python package, then you have a component that encapsulates the elements related to a specific feature of the application.

Unlike a Flask application, a Blueprint cannot be run on its own, it can only be registered on an app.

For example, imagine you wanted to create your app, and also expose the data in the database as an API for others. Both components could re-use an authentication package. You could create a blueprint for each of these components (main app, API, authentication) within your app.

To use a Blueprint within the example application, you will carry out the following:

1. Use the flask Blueprint class to create the blueprint
2. Import and register the blueprint in the application factory
3. Define routes to associate views with the Blueprint

## 1. Use the flask Blueprint class to create the blueprint

In practice, you are likely to have several modules that together form your Flask app. We are going to create only one module in this example, called 'main' for the core routes for the application. If you have a REST API and application functionality that uses it then you might want to separate the REST API routes into a separate Blueprint too.

If you have multiple blueprints you may want to add new Python packages within your project directory. For example (some files omitted for brevity):

```
/yourapplication
    /my_app
        __init__.py
        app.py
        /api
            __init__.py
        /main
            __init__.py
        /static
        /templates
```

If you are likely to have several modules that each have different templates, you may also want to add sub-directories to the templates folder for each module. Another structure you may encounter is to define the [templates and static folders within each module](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure). You may need to consider one of these for coursework 2, however for this practice example we will keep all the templates in the same directory.

The [Blueprint API documentation](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint) lists all the parameters you can define. A simple way to define a blueprint might look like the following:

```python
from flask import Blueprint

main_bp = Blueprint('main', __name__)
```

or for a REST API:

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='api')
```

The first example creates a blueprint called `main_bp` and defines one route (or view) called `index` within that Blueprint.

`url_prefix` is optional. This provides a path to prepend to all of the blueprint’s URLs, to make them distinct from the rest of the app’s routes.

Using the Flask app you created in `activities.md`, create the blueprint in `flask_app/hello.py`.

## 2. Import and register the blueprint in the application factory

Return to the `flask_app/__init__.py` file and the `create_app()` method.

After creating the Flask app, you need to register the blueprint before you return the Flask app object. You need to add the import within `create_app` to avoid circular imports. The code will look like something like this e.g.:

```python
def create_app(config_class_name):
    app = Flask(__name__)

    from flask_app.hello import main_bp
    app.register_blueprint(main_bp)

```

Note: if you are using a linter you will have to ignore the warnings that will suggest you move the import to the top of the file.

### 3. Define a route to associate a view with the Blueprint

Modify the `index` route in `hello.py` for this blueprint. You will no longer need `current_app` e.g.

```python
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')
```

Stop and restart the app and then navigate to: <http://127.0.0.1:5000/>

## Further examples

- [Flask documentation on blueprints](https://flask.palletsprojects.com/en/2.2.x/blueprints/#modular-applications-with-blueprints)
- [Miguel Gringerg: Using Blueprints as part of a better application structure](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure)
