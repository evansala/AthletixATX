import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # IMPORTANT: set a real secret key via the SECRET_KEY environment variable
    # before deploying. This fallback is only for local development.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "instance", "kinetix.db")
    )

    # The only two accounts allowed to exist on this site.
    # Passwords are NOT stored here -- they're set via seed_users.py.
    ALLOWED_USERS = {
        "josh@athletixatx.com": "Josh Kintigh",
        "admin@athletixatx.com": "Admin",
    }

    CATEGORIES = ["Workouts", "Coaching", "Nutrition", "DEXA"]

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME")
    CONTACT_RECIPIENT = "josh@athletixatx.com"
