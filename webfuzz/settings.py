"""Application Configuration."""

import os
from .utils import generate_secret_key


class Config:
    """Base Configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", generate_secret_key())
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # FFUF output path
    FFUF_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "webfuzz/tmp/ffuf_output")
    os.makedirs(FFUF_OUTPUT_PATH, exist_ok=True)
    # File size restriction
    MAX_CONTENT_LENGTH = 24 * 1024 * 1024  # 24 megabytes


class DevelopmentConfig(Config):
    """Development Configuration."""

    ENV = "dev"
    DEBUG = True


class ProductionConfig(Config):
    """Production Configuration."""

    ENV = "prod"
    DEBUG = False


class TestingConfig(Config):
    """Testing Configuration."""

    TESTING = True
    DEBUG = True


if os.environ.get("FLASK_ENV") == "production":
    config = ProductionConfig()
elif os.environ.get("FLASK_ENV") == "testing":
    config = TestingConfig()
else:
    config = DevelopmentConfig()
