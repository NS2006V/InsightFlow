"""
Application factory for InsightFlow.

Why a factory (create_app) instead of a single global `app = Flask(__name__)`:
- It lets us build the app with DIFFERENT configs (development / testing /
  production) without duplicating code.
- Tests can spin up a fresh app instance with TestingConfig, instead of
  reusing whatever config the running dev server happens to have.
"""

from flask import Flask

from app.config import config_by_name


def create_app(config_name="development"):
    """
    Build and configure a Flask application instance.

    Args:
        config_name (str): one of "development", "testing", "production".
                            Defaults to "development".

    Returns:
        Flask app instance, fully configured and with blueprints registered.
    """
    app = Flask(__name__)

    # Load the matching config class (see app/config.py)
    config_class = config_by_name.get(config_name, config_by_name["development"])
    app.config.from_object(config_class)

    # Register routes. Kept as a blueprint (not raw @app.route) so that
    # in later phases we can add more blueprints (upload, analytics, ...)
    # without this file growing unbounded.
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    return app
