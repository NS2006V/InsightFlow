"""
Main routes for InsightFlow.

Phase 0 only needs two routes:
- "/"       a home page confirming the app is running
- "/health" a machine-readable status check (useful later for
             deployment health checks on AWS, e.g. an ALB target group)

This is a Blueprint (not routes directly on `app`) so future phases can
add upload_routes.py, analytics_routes.py, etc. and register each as its
own blueprint in app/__init__.py, instead of one giant routes file.
"""

from flask import Blueprint, render_template, jsonify, current_app

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Simple landing page confirming InsightFlow is running."""
    return render_template("index.html", app_name=current_app.config["APP_NAME"])


@main_bp.route("/health")
def health():
    """
    Basic status endpoint.

    Returns JSON rather than HTML because this route is meant to be read
    by tools (uptime checks, load balancers), not by a person in a browser.
    """
    return jsonify(status="ok", app=current_app.config["APP_NAME"])
