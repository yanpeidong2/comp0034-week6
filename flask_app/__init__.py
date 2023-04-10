from flask import Flask

def create_app():

    app = Flask(hello)
    app.config["SECRET_KEY"] = "add_your_key_here"

    with app.app_context():
        from flask_app import hello

    return app
    