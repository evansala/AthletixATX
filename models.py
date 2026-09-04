from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db


def _parse_dt(value):
    """SQLite stores created_at as 'YYYY-MM-DD HH:MM:SS' text; parse it to a
    real datetime so templates can call .strftime() on it."""
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------- users ----
def get_user_by_email(email):
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email.strip().lower(),)).fetchone()
    return row


def get_user_by_id(user_id):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def verify_password(user_row, password):
    return check_password_hash(user_row["password_hash"], password)


def upsert_user_password(email, name, password):
    """Create the user if they don't exist, otherwise reset their password."""
    db = get_db()
    email = email.strip().lower()
    password_hash = generate_password_hash(password)
    existing = get_user_by_email(email)
    if existing:
        db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, existing["id"]))
        db.commit()
        return "updated"
    db.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (email, name, password_hash),
    )
    db.commit()
    return "created"


# --------------------------------------------------------------- videos ----
def list_videos():
    db = get_db()
    rows = db.execute(
        """
        SELECT videos.*, users.name AS author_name
        FROM videos
        JOIN users ON users.id = videos.author_id
        ORDER BY videos.created_at DESC, videos.id DESC
        """
    ).fetchall()

    videos = []
    for row in rows:
        d = dict(row)
        d["category_slug"] = d["category"].lower()
        d["embed_url"] = f"https://www.youtube.com/embed/{d['youtube_id']}"
        d["created_at"] = _parse_dt(d["created_at"])
        videos.append(d)
    return videos


def create_video(title, category, youtube_url, youtube_id, author_id):
    db = get_db()
    db.execute(
        """
        INSERT INTO videos (title, category, youtube_url, youtube_id, author_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, category, youtube_url, youtube_id, author_id),
    )
    db.commit()


def get_video(video_id):
    db = get_db()
    row = db.execute(
        """
        SELECT videos.*, users.name AS author_name
        FROM videos
        JOIN users ON users.id = videos.author_id
        WHERE videos.id = ?
        """,
        (video_id,),
    ).fetchone()
    if row is None:
        return None
    d = dict(row)
    d["category_slug"] = d["category"].lower()
    d["embed_url"] = f"https://www.youtube.com/embed/{d['youtube_id']}"
    d["created_at"] = _parse_dt(d["created_at"])
    return d


def update_video(video_id, title, category, youtube_url, youtube_id):
    db = get_db()
    db.execute(
        """
        UPDATE videos
        SET title = ?, category = ?, youtube_url = ?, youtube_id = ?
        WHERE id = ?
        """,
        (title, category, youtube_url, youtube_id, video_id),
    )
    db.commit()


def delete_video(video_id):
    db = get_db()
    db.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    db.commit()


# ------------------------------------------------------------- articles ----
def list_articles():
    db = get_db()
    rows = db.execute(
        """
        SELECT articles.*, users.name AS author_name
        FROM articles
        JOIN users ON users.id = articles.author_id
        ORDER BY articles.created_at DESC, articles.id DESC
        """
    ).fetchall()

    articles = []
    for row in rows:
        d = dict(row)
        text = d["body"].strip()
        d["excerpt"] = (text[:220] + "…") if len(text) > 220 else text
        d["created_at"] = _parse_dt(d["created_at"])
        articles.append(d)
    return articles


def get_article(article_id):
    db = get_db()
    row = db.execute(
        """
        SELECT articles.*, users.name AS author_name
        FROM articles
        JOIN users ON users.id = articles.author_id
        WHERE articles.id = ?
        """,
        (article_id,),
    ).fetchone()
    if row is None:
        return None
    d = dict(row)
    d["created_at"] = _parse_dt(d["created_at"])
    return d


def create_article(title, body, author_id):
    db = get_db()
    cur = db.execute(
        "INSERT INTO articles (title, body, author_id) VALUES (?, ?, ?)",
        (title, body, author_id),
    )
    db.commit()
    return cur.lastrowid


def update_article(article_id, title, body):
    db = get_db()
    db.execute(
        "UPDATE articles SET title = ?, body = ? WHERE id = ?",
        (title, body, article_id),
    )
    db.commit()


def delete_article(article_id):
    db = get_db()
    db.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    db.commit()
