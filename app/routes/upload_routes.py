"""
Upload routes.

This file only deals with HTTP and file objects -- reading the form,
grabbing the uploaded file, and rendering a template. All validation and
parsing logic lives in app/services/upload_service.py and
app/analytics/upload_validation.py, so this route function stays short
and easy to read.
"""

from flask import Blueprint, render_template, request

from app.services.upload_service import process_upload
from app.analytics.upload_validation import REQUIRED_COLUMNS

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():
    result = None

    if request.method == "POST":
        uploaded_file = request.files.get("dataset_file")
        result = process_upload(uploaded_file)

    return render_template("upload.html", result=result, required_columns=REQUIRED_COLUMNS)
