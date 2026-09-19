"""
Small, dependency-free helpers for checking an uploaded file's name
before we attempt to parse it with pandas.
"""

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def get_file_extension(filename):
    """Return the lowercase extension of filename (no dot), or "" if none."""
    if not filename or "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].lower()


def has_allowed_extension(filename):
    """True if filename ends in one of ALLOWED_EXTENSIONS (.csv / .xlsx)."""
    return get_file_extension(filename) in ALLOWED_EXTENSIONS
