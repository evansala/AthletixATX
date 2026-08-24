"""
Optional: imports the 5 sample videos that were hardcoded in the original
static videos.html, so the site isn't empty on first run. Attributes them to
josh@athletixatx.com. Safe to run more than once -- it skips videos that
already exist (matched by youtube_id).

Run this AFTER seed_users.py has created the accounts.

Usage:
    python seed_content.py
"""
from app import create_app
from db import get_db
from models import create_video, get_user_by_email

SAMPLE_VIDEOS = [
    ("Lateral Lunge at 74: Mobility, Balance & Strength", "GXFIKSqEQn4", "Workouts"),
    ("Lower Body Strength Block", "o6OKOOMkXHY", "Workouts"),
    ("Are You Eating Enough Protein?", "GjFLChZmYX0", "Nutrition"),
    ("Is Sourdough Bread Better?", "OpteieMn_5k", "Nutrition"),
    ("Dumbell Forward Lunge", "Y51qMyQL-y8", "Workouts"),
]


def main():
    app = create_app()
    with app.app_context():
        josh = get_user_by_email("josh@athletixatx.com")
        if not josh:
            print("josh@athletixatx.com doesn't exist yet -- run seed_users.py first.")
            return

        db = get_db()
        added = 0
        for title, yt_id, category in SAMPLE_VIDEOS:
            exists = db.execute("SELECT 1 FROM videos WHERE youtube_id = ?", (yt_id,)).fetchone()
            if exists:
                continue
            create_video(
                title=title,
                category=category,
                youtube_url=f"https://www.youtube.com/watch?v={yt_id}",
                youtube_id=yt_id,
                author_id=josh["id"],
            )
            added += 1
        print(f"Added {added} video(s). {len(SAMPLE_VIDEOS) - added} already existed.")


if __name__ == "__main__":
    main()
