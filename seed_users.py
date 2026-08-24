"""
Creates (or resets the password for) the two accounts allowed to log in:
  - josh@athletixatx.com
  - admin@athletixatx.com

There is no sign-up page anywhere in the app on purpose -- this script is the
only way accounts get created. Run it once when you set up the site, and again
any time you want to change a password.

Usage:
    python seed_users.py
"""
import getpass

from app import create_app
from models import get_user_by_email, upsert_user_password


def prompt_password(label):
    while True:
        pw1 = getpass.getpass(f"New password for {label}: ")
        if len(pw1) < 8:
            print("  Password must be at least 8 characters. Try again.")
            continue
        pw2 = getpass.getpass(f"Confirm password for {label}: ")
        if pw1 != pw2:
            print("  Passwords didn't match. Try again.")
            continue
        return pw1


def main():
    app = create_app()
    with app.app_context():
        for email, name in app.config["ALLOWED_USERS"].items():
            existing = get_user_by_email(email)
            if existing:
                print(f"\n{email} already exists.")
                answer = input("  Reset their password? [y/N]: ").strip().lower()
                if answer != "y":
                    continue
            else:
                print(f"\nCreating account for {email} ({name})")

            password = prompt_password(email)
            result = upsert_user_password(email, name, password)
            print(f"  {'Created' if result == 'created' else 'Updated'} {email}.")

    print("\nDone.")


if __name__ == "__main__":
    main()
