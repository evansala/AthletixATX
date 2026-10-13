from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_mail import Message

from extensions import mail

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/contact", methods=["POST"])
def contact():
    back = url_for("main.index") + "#contact"

    # Honeypot: real users never fill this hidden field
    if request.form.get("website"):
        return redirect(back)

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    goal = request.form.get("goal", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email:
        flash("Please include your name and email.", "error")
        return redirect(back)

    msg = Message(
        subject=f"Kinetix inquiry: {name} ({goal})",
        recipients=[current_app.config["CONTACT_RECIPIENT"]],
        reply_to=email,
        body=(
            f"Name:  {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone or '—'}\n"
            f"Goal:  {goal}\n\n"
            f"{message or '(no message)'}"
        ),
    )

    try:
        mail.send(msg)
        flash("[ MESSAGE RECEIVED ] We'll respond within 24 hours.", "success")
    except Exception:
        current_app.logger.exception("Contact form email failed")
        flash(
            "Something went wrong sending your message. "
            "Please call or text 512-739-7255.",
            "error",
        )

    return redirect(back)