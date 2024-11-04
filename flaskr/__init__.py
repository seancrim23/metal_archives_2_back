import os

from flask import Flask

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # simple hello page
    @app.route('/hello')
    def hello():
        return 'Hello World :)'

    from . import db
    db.init_app(app)
    from . import user
    app.register_blueprint(user.bp)
    from . import band
    app.register_blueprint(band.bp)
    from . import release
    app.register_blueprint(release.bp)
    from . import review
    app.register_blueprint(review.bp)
    from . import track
    app.register_blueprint(track.bp)
    app.add_url_rule('/', endpoint='index')

    return app