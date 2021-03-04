from flask import Flask
import os


def create_app():
    appl = Flask(__name__, static_folder=os.path.abspath(''))

    with appl.app_context():
        from Search import stack_overflow

        appl.register_blueprint(stack_overflow.stack_search_bp)

        return appl