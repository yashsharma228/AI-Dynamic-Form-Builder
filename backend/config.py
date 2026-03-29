import os
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs


def _build_db_uri():
    url = os.getenv("DATABASE_URL")
    if url:
        # Ensure PyMySQL driver is used (Railway / TiDB may give plain mysql://)
        if url.startswith("mysql://"):
            url = url.replace("mysql://", "mysql+pymysql://", 1)
        # TiDB Cloud requires SSL — append ssl params if not already present
        if "tidbcloud.com" in url and "ssl" not in url:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}ssl_verify_cert=true&ssl_verify_identity=true"
        return url
    # Fallback: construct from individual env vars (local dev)
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    db = os.getenv("MYSQL_DB", "dynamic_form_builder")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"


class Config:
    SQLALCHEMY_DATABASE_URI = _build_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
