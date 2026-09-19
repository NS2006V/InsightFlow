"""
Local development entry point.

Usage:
    python run.py

This reads CONFIG_NAME from the environment to decide which config class
to build the app with, and runs Flask's built-in dev server.
This file is NOT used in production — see wsgi.py for that.
"""

import os
from app import create_app

config_name = os.environ.get("CONFIG_NAME", "development")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config["DEBUG"])
