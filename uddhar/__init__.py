import os

from flask import Flask, request
import logging


def create_app(test_config=None):

    # logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = Flask(__name__, instance_relative_config=True)
    # placeholder secret_key, overwritten by reading from config file -- not tracked in git 
    app.config.from_mapping(
        SECRET_KEY="dev", 
        DATABASE=os.path.join(app.instance_path, 'uddhari.sqlite'),
    )

    app.config.from_json('development.json')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import friend
    app.register_blueprint(friend.bp)


    @app.before_request
    def logrequest():
        app.logger.debug("%s",request)
        app.logger.debug("%s",request.get_json())

    @app.after_request
    def logresponse(response):
        app.logger.debug(response)
        app.logger.debug("%s",response.get_json())
        return response

    return app

