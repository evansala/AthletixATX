import os

from flask import Flask, g

import db as db_module
from auth_utils import load_logged_in_user
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)

    db_module.init_app(app)
    db_module.init_db(app)

    from main import bp as main_bp
    from auth import bp as auth_bp
    from videos import bp as videos_bp
    from articles import bp as articles_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(articles_bp)

    app.before_request(load_logged_in_user)

    @app.context_processor
    def inject_globals():
        return {"nav_categories": app.config["CATEGORIES"], "current_user": g.user}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
