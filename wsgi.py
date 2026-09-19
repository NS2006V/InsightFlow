"""
WSGI entry point for production servers (e.g. Gunicorn on AWS EC2).

Example:
    gunicorn --bind 0.0.0.0:8000 wsgi:app

Gunicorn imports the `app` object from this file directly, so unlike
run.py there is no __main__ block or dev server call here.
"""

import os
from app import create_app

config_name = os.environ.get("CONFIG_NAME", "production")
app = create_app(config_name)
