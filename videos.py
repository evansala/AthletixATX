from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for

from auth_utils import login_required
from models import create_video, delete_video, get_video, list_videos, update_video
from youtube_utils import extract_youtube_id

bp = Blueprint("videos", __name__, url_prefix="/videos")


@bp.route("/")
def index():
    all_videos = list_videos()
    recent = all_videos[:6]
    archive = all_videos[6:]
    categories = current_app.config["CATEGORIES"]
    return render_template(
        "videos.html", recent=recent, archive=archive, categories=categories
    )


@bp.route("/post", methods=["GET", "POST"])
@login_required
def post():
    categories = current_app.config["CATEGORIES"]

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        category = (request.form.get("category") or "").strip()
        youtube_url = (request.form.get("youtube_url") or "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if category not in categories:
            errors.append("Please select a category.")
        youtube_id = extract_youtube_id(youtube_url)
        if not youtube_url:
            errors.append("A YouTube link is required.")
        elif not youtube_id:
            errors.append("That doesn't look like a valid YouTube link.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template(
                "post_video.html",
                categories=categories,
                form_data={"title": title, "category": category, "youtube_url": youtube_url},
            ), 400

        create_video(
            title=title,
            category=category,
            youtube_url=youtube_url,
            youtube_id=youtube_id,
            author_id=g.user.id,
        )
        flash("Video posted.", "success")
        return redirect(url_for("videos.index"))

    return render_template("post_video.html", categories=categories, form_data={})


@bp.route("/<int:video_id>/edit", methods=["GET", "POST"])
@login_required
def edit(video_id):
    video = get_video(video_id)
    if not video:
        abort(404)
    categories = current_app.config["CATEGORIES"]

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        category = (request.form.get("category") or "").strip()
        youtube_url = (request.form.get("youtube_url") or "").strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if category not in categories:
            errors.append("Please select a category.")
        youtube_id = extract_youtube_id(youtube_url)
        if not youtube_url:
            errors.append("A YouTube link is required.")
        elif not youtube_id:
            errors.append("That doesn't look like a valid YouTube link.")

        if errors:
            for e in errors:
                flash(e, "error")
            video.update({"title": title, "category": category, "youtube_url": youtube_url})
            return render_template(
                "edit_video.html", categories=categories, video=video
            ), 400

        update_video(video_id, title=title, category=category, youtube_url=youtube_url, youtube_id=youtube_id)
        flash("Video updated.", "success")
        return redirect(url_for("videos.index"))

    return render_template("edit_video.html", categories=categories, video=video)


@bp.route("/<int:video_id>/delete", methods=["POST"])
@login_required
def delete(video_id):
    video = get_video(video_id)
    if not video:
        abort(404)
    delete_video(video_id)
    flash("Video deleted.", "success")
    return redirect(url_for("videos.index"))
