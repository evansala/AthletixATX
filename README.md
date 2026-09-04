# Kinetix Performance Coaching — Flask App

## What this is

Your static site turned into a Flask app, plus:

- An intro video embedded immediately below the full-screen banner on the homepage (placeholder — swap it out when you have the real one).
- Login for exactly two accounts — `josh@athletixatx.com` and `admin@athletixatx.com`. There is no sign-up page anywhere; accounts only get created by you, from the command line.
- **Post Video**: either account can paste a YouTube link, give it a title, and pick a category (Workouts / Coaching / Nutrition / DEXA). All three are required — if you try to submit without them, a popup blocks you and lists what's missing. Once submitted, the video shows up on the `/videos` page in the grid, filterable by category, same as every other video.
- **Write Article**: either account can write a blog post right in the browser (title + body). Title is mandatory. It publishes to a new `/articles` page, with each post getting its own detail page.
- "+ Post Video" and "+ Write Article" links are in the nav on every page whenever you're logged in, so you can jump to either from anywhere.
- **Edit / delete**: while logged in (either account), an "Edit" link appears on every video card and article card, and on the article detail page. Editing reuses the same required-field validation as posting. Delete asks for a plain browser confirmation first, then removes it for good. Either account can edit or delete anything — posts aren't locked to whoever created them.
- The featured video at the top of `/videos` is a separate placeholder embed (per your note that you'll add the real intro video later) — it isn't pulled from the database.

## 1. Install

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Create the two logins

There's no sign-up form on purpose — this script is the only way accounts get made or passwords get changed:

```bash
python seed_users.py
```

It'll prompt you for a password for `josh@athletixatx.com` and `admin@athletixatx.com` (minimum 8 characters). Run it again any time you want to reset a password.

## 3. (Optional) Import the 5 sample videos from the old site

So the video grid isn't empty on first run:

```bash
python seed_content.py
```

## 4. Add your real images

The templates still point at the same paths the static site used:

- `static/images/logo-circle.jpg` — the round logo (nav + footer)
- `static/images/logo-banner.jpg` — the full-screen banner image

Drop your real files in at those paths.

## 5. Run it

```bash
python app.py
```

Visit `http://127.0.0.1:5000`.

## 6. Set a real secret key before deploying

Locally, `app.py` falls back to a dev-only secret key. Before you put this anywhere public, set a real one:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

(On Windows, generate the value the same way and set it with `set SECRET_KEY=...` or your host's environment variable settings.)

## Notes

- The database is SQLite, stored at `instance/kinetix.db`, created automatically the first time the app runs.
- YouTube links are parsed to accept `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/embed/`, and `youtube.com/shorts/` formats.
- Both the server and the browser validate the Post Video / Write Article forms, so nothing incomplete can be saved even if someone bypasses the JS.
- Categories live in `config.py` (`CATEGORIES`) — add or rename one there and it flows through to the dropdown, the filter bar, and the video grid automatically.
