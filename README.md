# 🎬 CineLog
A cinephile's film journal and community platform. Log every film you've watched,
write reviews, build watchlists, and discover films through community curation.
**Live Demo:** https://your-app-name.up.railway.app

---

## Features
- Browse and search a catalog of films by title, director, and genre
- Write and manage personal film reviews with ratings (1–10)
- Build public or private watchlists and track watched/unwatched entries
- User profiles with bio, avatar, and favourite genre
- Two user groups: **Critics** (can add/edit films) and **Members** (standard users)
- RESTful API for films, genres, and reviews
- Asynchronous task processing with Celery — welcome emails,
  review notifications, weekly watchlist digest, nightly rating updates
- Fully responsive Bootstrap 5 design
- Custom 404 and 500 error pages

---

## Tech Stack
- **Backend:** Django 5.x, Django REST Framework
- **Database:** PostgreSQL
- **Async Tasks:** Celery + Redis + django-celery-beat
- **Frontend:** Django Template Engine + Bootstrap 5
- **Deployment:** Railway
- **Storage:** WhiteNoise (static files)

---

## Local Setup

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis (or Docker)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/cinelog.git
cd cinelog
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:
```bash
cp .env.example .env
```

### 5. Set up the database

Create a PostgreSQL database and user, then run migrations:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

### 7. Run Celery (optional for local async tasks)

In a separate terminal:
```bash
celery -A config worker --loglevel=info
```

For periodic tasks:
```bash
celery -A config beat --loglevel=info
```

---

## Environment Variables

Create a `.env` file in the project root with the following variables:
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=cinelog_db
DB_USER=cinelog_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (console backend for local dev)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@cinelog.com
```

---

## Running Tests
```bash
python manage.py test
```
Expected output: 23 tests, 0 failures.

---
Project structure
cinelog/
├── accounts/        # Custom user model, auth, profiles
├── api/             # Django REST Framework endpoints
├── config/          # Project settings, URLs, Celery config
├── core/            # Landing page, shared utilities
├── films/           # Film, Genre, CastMember models and views
├── reviews/         # Review and ReviewComment models and views
├── watchlists/      # Watchlist and WatchlistEntry models and views
├── static/          # CSS, JS, images
├── templates/       # All HTML templates
├── media/           # User uploaded files (local dev only)
├── manage.py
├── requirements.txt
├── Procfile
└── README.md

---

## API Endpoints
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/` | API root | No |
| GET | `/api/movies/` | List all movies | No |
| GET | `/api/movies/<id>/` | Movie detail | No |
| GET/POST | `/api/movies/<id>/reviews/` | List/create reviews | Read: No, Write: Yes |
| GET | `/api/genres/` | List all genres | No |

---

## Deployment
This project is deployed on **Railway** with:
- PostgreSQL database provisioned by Railway
- Redis instance provisioned by Railway
- Automatic deployments on push to `main`
- WhiteNoise for static file serving
- Gunicorn as the WSGI server
---

## Known Limitations
- Media files (uploaded posters, avatars) are not persisted across
  redeployments due to Railway's ephemeral filesystem.
  A production-grade solution would integrate AWS S3 or Cloudinary.

---

## Author
**Georgi Malchov** — SoftUni Django Advanced Regular Exam, April 2026

## Project Structure
