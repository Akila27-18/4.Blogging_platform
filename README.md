
# Blogging Platform (Django)

A fully functional blogging platform with posts, comments (moderation), categories, authentication, pagination, search, image upload, signals, and email (console backend). Uses Bootstrap and Roboto font. Responsive and clean.

## Features
- Posts: create, edit, delete (author-only), image uploads, slugs
- Comments: submit; staff can moderate (approve)
- Categories: many-to-many, filter on list
- Authentication: login, logout, register
- Password reset via Django email (console backend)
- Signals: email when new comment is added; email alert on new post
- Pagination, search
- Admin customization
- Sample data via management command

## Quick Start
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed  # creates sample users, categories, posts, comments
Log in with:

admin / admin12345

alice / pass12345

bob / pass12345
# Users: alice/bob (pass12345), admin (admin12345)

python manage.py runserver
```

Login to see posts. Create/upload images in forms. Password reset emails appear in console.
