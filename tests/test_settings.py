from core_main_app.utils.databases.mongoengine_database import Database

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    # Local apps
    "tests",
]

CUSTOM_NAME = "Local"
""" :py:class:`str`: Name of the local instance
"""

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}


MOCK_DATABASE_NAME = "db_mock"
MOCK_DATABASE_HOST = "mongomock://localhost"

database = Database(MOCK_DATABASE_HOST, MOCK_DATABASE_NAME)
database.connect()
