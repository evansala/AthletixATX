from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from models import get_user_by_email, verify_password

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = get_user_by_email(email)
        if user and verify_password(user, password):
            session.clear()
            session["user_id"] = user["id"]
            flash(f"Welcome back, {user['name']}.", "success")
            next_url = request.args.get("next")
            return redirect(next_url or url_for("main.index"))

        flash("Incorrect email or password.", "error")

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You've been logged out.", "success")
    return redirect(url_for("main.index"))
