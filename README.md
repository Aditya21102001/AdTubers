# AdTubers

A Django web app that acts as a bridge between **content creators** and **event
organizers**.

### Problem
Content creators are looking for people who will hire their talents, and event
organizers need creators to add entertainment to their events — but the two
communities lack any link between them.

### Solution
A full-stack website that connects the two. Creators get events to perform at and
earn a livelihood, while organizers get a platform to discover and hire them.

---

## Tech stack

| Layer     | Technology                                   |
| --------- | -------------------------------------------- |
| Backend   | Python 3.11+ · Django 5.2 (LTS)              |
| Auth      | Django auth · django-allauth (Google/Facebook social login) |
| Frontend  | HTML · CSS · Bootstrap 4                      |
| Rich text | django-ckeditor                              |
| Database  | SQLite (default, zero-config) · PostgreSQL (optional) |

> **Note:** the project was originally built on Django 3.2 / Python 3.9 and has
> been modernized to run on Django 5.2 and Python 3.13. See
> [What was modernized](#what-was-modernized) below.

---

## Getting started (local)

Requires **Python 3.11+** (tested on 3.13). All commands are run from the
`tubers/` directory unless noted.

### 1. Clone and create a virtual environment

```bash
git clone <your-fork-url> AdTubers
cd AdTubers/tubers

python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r ../requirements.txt
```

### 3. Set up the database and demo data

The project defaults to **SQLite**, so no database server is needed.

```bash
python manage.py migrate
python manage.py seed_demo   # optional: superuser + sample creators/team/sliders
```

`seed_demo` is idempotent and creates a superuser (default `admin` / `admin` —
override with `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_PASSWORD`). To
create the superuser yourself instead, run `python manage.py createsuperuser`.

### 4. Run the server

```bash
python manage.py runserver
```

- App:   http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/  (log in with the seeded `admin` account)

---

## Configuration

Settings read from environment variables, with development-friendly defaults:

| Variable                     | Default                          | Purpose                          |
| ---------------------------- | -------------------------------- | -------------------------------- |
| `DJANGO_SECRET_KEY`          | insecure dev key                 | **Set a real value in production** |
| `DJANGO_DEBUG`               | `True`                           | Set `False` in production        |
| `DJANGO_ALLOWED_HOSTS`       | `localhost,127.0.0.1,[::1]`      | Comma-separated hosts            |
| `DJANGO_CSRF_TRUSTED_ORIGINS`| _(empty)_                        | Comma-separated origins          |
| `DB_ENGINE`                  | `sqlite`                         | Set to `postgres` for PostgreSQL |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | — | PostgreSQL connection            |

### Using PostgreSQL

```bash
pip install "psycopg[binary]"
export DB_ENGINE=postgres DB_NAME=lcotubers DB_USER=postgres DB_PASSWORD=... DB_HOST=localhost
python manage.py migrate
```

### Social login (Google / Facebook)

Social login buttons appear automatically **once you configure a provider**.
Add a *Social Application* for Google and/or Facebook under
`/admin/socialaccount/socialapp/` with your OAuth credentials. Until then the
login/register pages work normally without the social buttons.

---

## Project structure

```
tubers/
├── accounts/       # custom login / register / dashboard
├── webpages/       # home, about, services, contact + Team/Slider models + seed_demo
├── youtubers/      # creator listing, detail, search (Youtuber model)
├── hiretubers/     # "hire a creator" enquiry form
├── contactpage/    # public contact form
├── contactinfo/    # site-wide contact details shown in header/footer
├── templates/      # shared + per-app templates
├── tubers/         # project settings, urls, wsgi/asgi, source static assets
└── manage.py
```

---

## What was modernized

The codebase was updated from its original 2021 state:

- **Django 3.2 → 5.2 (LTS)** and verified on **Python 3.13**; dependencies pinned
  in `requirements.txt` / `Pipfile`.
- **Fixed a startup crash**: `urls.py` referenced `MEDIA_URL` / `MEDIA_ROOT`,
  which were never defined in settings.
- **Fixed broken `__str__` methods** on the `Hiretuber`, `Contactpage`, and
  `Contactinfo` models (they were indented at module level, outside the class).
- **Hardened views**: pages no longer 500 when no `Contactinfo` row exists
  (`latest('id')` → `last()`).
- **Fixed the `vedio_url` typo** → `video_url`.
- **Cleaned model fields**: removed a meaningless `max_length` on a `BooleanField`,
  switched naive `datetime.now` defaults to timezone-aware `timezone.now`, and
  removed the redundant `media/` prefix from `upload_to` paths.
- **Updated django-allauth** to v65 (added the required `AccountMiddleware` and
  auth backend) and rewrote the social-login buttons to render only for
  configured providers, so the auth pages no longer crash when OAuth isn't set up.
- **Local-first config**: defaults to SQLite, secrets/hosts read from the
  environment, and an idempotent `seed_demo` management command.
- Added `.gitignore` and removed the stale `Pipfile.lock`.

### Known follow-up

`django-ckeditor` bundles **CKEditor 4**, which is end-of-life and has known
security issues. It is only used for admin-managed rich-text description fields
here. Consider migrating to
[`django-ckeditor-5`](https://pypi.org/project/django-ckeditor-5/) (check the
CKEditor 5 license terms first) or the paid CKEditor 4 LTS package.

---

## Screenshots

Home Page
![home](https://user-images.githubusercontent.com/54741890/143493205-e2f0722a-63a1-4d58-9472-930ace8bb689.png)

Login Page
![login](https://user-images.githubusercontent.com/54741890/143493363-52f569f1-c0c2-4678-8eb7-b3b12f066561.png)

Sign Up Page
![signup](https://user-images.githubusercontent.com/54741890/143493414-8328824b-4f84-4b84-a0c1-025ed6366720.png)

Admin
![admin](https://user-images.githubusercontent.com/54741890/143493442-9c7f38b9-4e7b-4d37-b027-ea27aa0a1602.png)

Data Flow Diagram:
https://coggle.it/diagram/YUxCKcXUaXxGha8H/t/-/ec17542f709d625778279ebcf77fb9494c46b52c526064ac830b59382194fbbd
