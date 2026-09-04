from functools import wraps

from flask import g, redirect, request, session, url_for

from models import get_user_by_id


class CurrentUser:
    """Simple attribute-access wrapper so templates can do current_user.name
    whether or not someone is logged in."""

    def __init__(self, id=None, email=None, name=None, is_authenticated=False):
        self.id = id
        self.email = email
        self.name = name
        self.is_authenticated = is_authenticated


def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = CurrentUser()
        return

    row = get_user_by_id(user_id)
    if row is None:
        session.clear()
        g.user = CurrentUser()
        return

    g.user = CurrentUser(id=row["id"], email=row["email"], name=row["name"], is_authenticated=True)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.user.is_authenticated:
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped
