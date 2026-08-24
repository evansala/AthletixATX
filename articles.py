from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from auth_utils import login_required
from models import create_article, delete_article, get_article, list_articles, update_article

bp = Blueprint("articles", __name__, url_prefix="/articles")


@bp.route("/")
def index():
    all_articles = list_articles()
    return render_template("articles.html", articles=all_articles)


@bp.route("/<int:article_id>")
def detail(article_id):
    article = get_article(article_id)
    if not article:
        abort(404)
    return render_template("article_detail.html", article=article)


@bp.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not body:
            errors.append("The article can't be empty.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template(
                "write_article.html", form_data={"title": title, "body": body}
            ), 400

        article_id = create_article(title=title, body=body, author_id=g.user.id)
        flash("Article published.", "success")
        return redirect(url_for("articles.detail", article_id=article_id))

    return render_template("write_article.html", form_data={})


@bp.route("/<int:article_id>/edit", methods=["GET", "POST"])
@login_required
def edit(article_id):
    article = get_article(article_id)
    if not article:
        abort(404)

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        body = (request.form.get("body") or "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not body:
            errors.append("The article can't be empty.")

        if errors:
            for e in errors:
                flash(e, "error")
            article.update({"title": title, "body": body})
            return render_template("edit_article.html", article=article), 400

        update_article(article_id, title=title, body=body)
        flash("Article updated.", "success")
        return redirect(url_for("articles.detail", article_id=article_id))

    return render_template("edit_article.html", article=article)


@bp.route("/<int:article_id>/delete", methods=["POST"])
@login_required
def delete(article_id):
    article = get_article(article_id)
    if not article:
        abort(404)
    delete_article(article_id)
    flash("Article deleted.", "success")
    return redirect(url_for("articles.index"))
