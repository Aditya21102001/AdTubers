# AdTuber — Architecture (in simple words)

This document explains how the whole AdTuber application is put together, in plain
language. If you have never seen this codebase before, start here. For setup and
run instructions see [README.md](README.md).

---

## 1. What is AdTuber?

AdTuber is a **website that connects two groups of people who normally can't find
each other**:

- **Content creators** (YouTubers) who want to be hired for events.
- **Event organizers / brands** who want creators to entertain or promote at their
  events.

The site lets a visitor **browse creators**, **filter and search** them, get an
**AI-powered match** for their event, and **send a "hire me" request**. Behind the
scenes, an **admin** manages all the creators, team members, banners, and incoming
booking requests through Django's admin panel.

Think of it as a small marketplace: the public side is a catalogue + contact form,
and the private side is an admin dashboard.

---

## 2. The big picture

AdTuber is a **classic server-rendered web app** built with **Django** (a Python web
framework). There is no separate frontend framework — the server builds complete HTML
pages and sends them to the browser.

```
┌──────────────┐     HTTP request      ┌───────────────────────────┐     SQL      ┌──────────────┐
│              │  ───────────────────> │                           │  ─────────>  │              │
│   Browser    │                       │   Django (AdTuber apps)   │              │   Database   │
│  (visitor)   │  <─────────────────── │                           │  <────────  │  SQLite/     │
│              │    HTML page back      │                           │   rows       │  PostgreSQL  │
└──────────────┘                       └───────────────────────────┘              └──────────────┘
                                              │        ▲
                                        reads │        │ renders
                                              ▼        │
                                       ┌────────────────────────┐
                                       │  Templates (HTML) +    │
                                       │  static CSS / JS /     │
                                       │  uploaded media images │
                                       └────────────────────────┘
```

Django follows the **MVT pattern** (Model–View–Template), which is Django's take on
MVC:

| Piece        | What it is                                    | In this project                          |
| ------------ | --------------------------------------------- | ---------------------------------------- |
| **Model**    | A Python class describing a database table    | `Youtuber`, `Team`, `Hiretuber`, …       |
| **View**     | A Python function that handles one request    | `youtubers()`, `home()`, `recommend()`   |
| **Template** | An HTML file with placeholders for data       | `youtubers.html`, `home.html`, …         |
| **URL conf** | A map from a web address to a view            | each app's `urls.py`                     |

**The one-line summary of every request:** a URL points to a view, the view reads
models from the database, then hands the data to a template that renders the HTML.

### Tech stack

| Layer        | Technology                                                        |
| ------------ | ----------------------------------------------------------------- |
| Language     | Python 3.11+ (tested on 3.13)                                     |
| Framework    | Django 5.2 (LTS)                                                   |
| Auth         | Django's built-in auth **+** django-allauth (Google/Facebook login)|
| Rich text    | django-ckeditor-5 (admin rich-text description fields)            |
| Frontend     | Server-rendered HTML + Bootstrap 4 + a little jQuery/Slick        |
| Database     | SQLite by default (zero-config); PostgreSQL in production         |
| Static files | WhiteNoise (serves CSS/JS straight from the app process)         |
| Server       | Django dev server locally; Gunicorn in production                |
| Deployment   | Docker image, deployed free on Render                            |
| AI match     | Pure-Python TF-IDF recommender (no external AI service)          |

Everything is **open-source and free of cost** — there are no paid APIs or services.

---

## 3. How the project is organized (Django apps)

Django encourages splitting a project into small, focused **apps**. AdTuber has one
Django *project* (`tubers`) that ties together **six custom apps**, each owning one
slice of the product:

```
tubers/                         ← the Django PROJECT (settings, root URLs, wsgi/asgi)
├── webpages/     ← the public marketing pages (home, about, services, contact)
│                   + owns the Team and Slider models + the seed_demo command
├── youtubers/    ← the creator catalogue: list, detail, search, AI match
├── hiretubers/   ← the "hire this creator" booking request form
├── accounts/     ← custom login / register / logout / user dashboard
├── contactpage/  ← stores messages sent from the public contact form
└── contactinfo/  ← site-wide contact details shown in the header & footer
```

Here is what each app is responsible for and the main pieces inside it:

| App             | Owns model(s)        | Public URLs                                   | Job in one sentence                                                        |
| --------------- | -------------------- | --------------------------------------------- | -------------------------------------------------------------------------- |
| **webpages**    | `Team`, `Slider`     | `/`, `/about`, `/services`, `/contact`        | Renders the marketing pages and holds homepage banners + team profiles.    |
| **youtubers**   | `Youtuber`           | `/youtubers/`, `/youtubers/<id>`, `/youtubers/search`, `/youtubers/recommend` | The heart of the site: browse, view, search, and AI-match creators.        |
| **hiretubers**  | `Hiretuber`          | `/hiretubers/hiretuber` (POST)                | Receives a booking request from a creator's detail page and saves it.      |
| **accounts**    | *(uses Django's `User`)* | `/accounts/login`, `/register`, `/logout`, `/dashboard` | Handles sign-up, sign-in, and a dashboard listing the user's bookings.     |
| **contactpage** | `Contactpage`        | `/contactpage/` (POST)                        | Saves a general message from the site's contact form.                      |
| **contactinfo** | `Contactinfo`        | `/contactinfo/` (POST)                        | One row of site-wide contact/social details injected into every page.      |

### How the apps talk to each other

The apps are loosely coupled. A few cross-app references worth knowing:

- **`contactinfo` is used everywhere.** Almost every view loads the single
  `Contactinfo` row and passes it to the template, because the shared **header** and
  **footer** display the site email, phone, and social links.
- **`webpages.home` and `youtubers` both read the `Youtuber` model** — the homepage
  shows featured creators, the youtubers app shows all of them.
- **`accounts.dashboard` reads `Hiretuber`** — it lists the bookings a logged-in user
  submitted.
- Bookings link to creators and users **by plain ID number, not by a database
  foreign key** (`Hiretuber.tuber_id`, `Hiretuber.user_id` are just integers). This
  keeps the apps decoupled but means the database does not enforce those links.

---

## 4. The data (models)

Six custom tables, plus Django's built-in `User` table. None of the custom models use
foreign keys — relationships are by convention (matching ID values), not enforced by
the database.

```
┌─────────────────────────┐         ┌──────────────────────────┐
│ Youtuber (youtubers)    │         │ User (Django built-in)   │
│─────────────────────────│         │──────────────────────────│
│ name, price, photo      │         │ username, email, password│
│ video_url, description  │         └──────────────────────────┘
│ city, age, height       │                    │ (by user_id)
│ crew, camera_type       │                    │
│ subs_count, category    │         ┌──────────┴───────────────┐
│ is_featured, created…   │◄────────│ Hiretuber (hiretubers)   │
└─────────────────────────┘ (by     │──────────────────────────│
                          tuber_id)  │ first/last name, email   │
                                     │ tuber_id, tuber_name     │
┌─────────────────────────┐         │ city, state, phone       │
│ Team (webpages)         │         │ message, status          │
│ first/last name, role   │         │ user_id, created_date    │
│ photo, social links     │         └──────────────────────────┘
└─────────────────────────┘
                                     ┌──────────────────────────┐
┌─────────────────────────┐         │ Contactpage (contactpage)│
│ Slider (webpages)       │         │ name, subject, phone,    │
│ headerline, subtitle    │         │ email, message, …        │
│ button_text, photo,link │         └──────────────────────────┘
└─────────────────────────┘
                                     ┌──────────────────────────┐
                                     │ Contactinfo (contactinfo)│  ← single row,
                                     │ name, phone, email,      │    shown site-wide
                                     │ social handles, 2× rich  │
                                     │ text descriptions        │
                                     └──────────────────────────┘
```

| Model         | Managed by            | What one row represents                                            |
| ------------- | --------------------- | ------------------------------------------------------------------ |
| `Youtuber`    | Admin                 | One creator listed in the catalogue (photo, price, category, …).   |
| `Team`        | Admin                 | One "About us" team member (name, role, photo, social links).      |
| `Slider`      | Admin                 | One homepage carousel banner (headline, subtitle, button, image).  |
| `Hiretuber`   | Public form → Admin   | One booking/hire request, with a `pending/accepted/declined` status. |
| `Contactpage` | Public form → Admin   | One message from the general contact form.                         |
| `Contactinfo` | Admin (single row)    | The site's own contact + social details (used in header/footer).   |
| `User`        | Auth / self sign-up   | A registered visitor who can log in and see their dashboard.       |

**Rich text:** `Youtuber.description` and the two `Contactinfo` descriptions use a
CKEditor 5 field, so the admin can write formatted HTML. Templates render these with
`| safe`, and the AI recommender strips the HTML tags before matching.

---

## 5. How a page actually loads (request lifecycle)

Let's trace a visitor opening the creator list at `/youtubers/`:

```
1. Browser requests  GET /youtubers/
        │
2. tubers/urls.py  →  routes "/youtubers/..." to youtubers/urls.py
        │
3. youtubers/urls.py  →  "" maps to the views.youtubers function
        │
4. views.youtubers(request):
        ├── reads Youtuber rows from the DB (newest first)
        ├── applies keyword/city/camera/category filters from the URL's GET params
        ├── paginates to 8 per page
        ├── loads the Contactinfo row (for header/footer)
        └── builds a "context" dict of data
        │
5. render(request, 'youtubers/youtubers.html', context)
        ├── youtubers.html  extends  base.html
        ├── base.html  includes  header.html, navbar.html, footer.html
        └── Django fills placeholders with the context data
        │
6. Finished HTML page  →  sent back to the browser
```

Every page in the site follows this same shape. The shared layout lives in
`templates/base.html`, which pulls in the header, navbar, and footer partials, so
individual page templates only fill in the `{% block content %}`.

### Two kinds of views in this codebase

1. **Page views (GET)** — build a context and render a template. Example: `home`,
   `about`, `youtubers`, `youtubers_detail`, `recommend`.
2. **Form-handler views (POST)** — read submitted form fields, save a model row, flash
   a success message, and redirect. Example: `hiretuber`, `contactpage`, `register`,
   `login`. These follow the **Post/Redirect/Get** pattern so a refresh doesn't
   resubmit the form.

---

## 6. Key user journeys

### A. Browse & search creators
`Home / navbar → /youtubers/` shows a paginated grid. The search dropdowns filter by
**city, camera type, and category**, and a keyword box matches text inside the
description. Filters are carried in the URL's query string, so pagination links keep
the active filters (see `templates/includes/pagination.html`).

### B. AI Creator Match  ⭐
`Navbar → "AI Match" → /youtubers/recommend`. The visitor types a free-text brief
("a funny gaming creator in Delhi for a product launch") and the app ranks creators by
relevance, showing a **match % score** and the words that matched. Explained in
detail in section 7.

### C. Hire a creator
`/youtubers/<id>` (detail page) has a **"Fill the Form and reach out"** form. Submitting
it POSTs to the `hiretubers` app, which saves a `Hiretuber` row with status
`pending`. If the visitor is logged in, their user id is attached so the booking shows
up on their dashboard.

### D. Sign up / sign in / dashboard
The **accounts** app provides custom login and register pages (plain Django forms, not
allauth's default pages). django-allauth is wired in for optional **Google/Facebook**
social login — the buttons only appear once an admin configures a provider. A
logged-in user's **dashboard** lists the bookings they submitted, with each booking's
current status.

### E. Admin manages everything
`/admin/` is Django's admin, styled with djangocms-admin-style. Admins create/edit
creators, team members, and sliders; edit the site's contact info; and review incoming
bookings and contact messages. The `Hiretuber` admin adds bulk **"Mark accepted /
declined"** actions and inline status editing.

---

## 7. The "AI Creator Match" explained simply

The AI match lives in [`tubers/youtubers/recommender.py`](tubers/youtubers/recommender.py)
and is deliberately **simple, dependency-free, and free to run** — no external AI API,
no numpy/scikit-learn, so it fits inside Render's free 512 MB tier.

It uses a classic information-retrieval technique called **TF-IDF cosine similarity**.
In plain words:

1. **Build a text profile** for every creator by joining their name, category, city,
   camera, crew, and (HTML-stripped) description into one string.
2. **Tokenize** the search brief and each profile into words, dropping common filler
   words ("the", "for", "event", …) via a small stopword list.
3. **Score words by importance (TF-IDF).** A word that appears in *this* creator a lot
   but is *rare across all creators* gets a high weight; a word everyone shares gets a
   low weight.
4. **Compare** the brief's word-vector to each creator's word-vector using **cosine
   similarity** (how much the two point in the same direction).
5. **Rank** creators by that similarity, convert it to a **0–100% match score**, and
   return the top 6 — along with the top few matched words for display.

The `views.recommend` view calls `rank_youtubers(query, Youtuber.objects.all())` and
passes the ranked results to `recommend.html`, which draws the score bars and matched
tags. Because the interface is a single function, you could later swap in
scikit-learn or sentence-transformer embeddings without changing the view.

---

## 8. Configuration & environments

All configuration lives in [`tubers/tubers/settings.py`](tubers/tubers/settings.py) and
is driven by **environment variables with safe local defaults**, so the project runs
with zero setup locally but hardens automatically in production.

| Variable                      | Default                     | Purpose                               |
| ----------------------------- | --------------------------- | ------------------------------------- |
| `DJANGO_SECRET_KEY`           | insecure dev key            | Cryptographic signing (set in prod).  |
| `DJANGO_DEBUG`                | `True`                      | Verbose errors; **`False` in prod**.  |
| `DJANGO_ALLOWED_HOSTS`        | `localhost,127.0.0.1,[::1]` | Which hostnames may serve the app.    |
| `DATABASE_URL` / `DB_*`       | SQLite                      | Database connection (see below).      |
| `DJANGO_SECURE_SSL_REDIRECT`  | `False`                     | Force HTTPS + secure cookies in prod. |
| `SEED_DEMO`                   | —                           | If `true`, seed demo data on startup. |
| `DJANGO_SUPERUSER_*`          | `admin` / `admin`           | Credentials the seed command uses.    |

**Database selection** (priority order, in `settings.py`):
1. `DATABASE_URL` present → use it (Render/Heroku-style Postgres).
2. else `DB_ENGINE=postgres` → build a Postgres config from `DB_*` vars.
3. else → **SQLite** file (`db.sqlite3`) — the local default.

**Demo data:** `python manage.py seed_demo`
([`webpages/management/commands/seed_demo.py`](tubers/webpages/management/commands/seed_demo.py))
is idempotent — it creates a superuser plus sample sliders, team members, and
creators, and can be re-run safely.

---

## 9. Deployment

The app ships as a **Docker image** and deploys to **Render** for free.

```
render.yaml (Blueprint)
   │  declares: a web service (Docker) + a free Postgres database
   ▼
Dockerfile  (python:3.13-slim)
   1. pip install -r requirements.txt      (cached layer)
   2. COPY the Django project
   3. collectstatic  → WhiteNoise bakes static files into the image
   4. on start:  migrate → (optional) seed_demo → gunicorn serves the app
   ▼
Render
   • injects DATABASE_URL (managed Postgres) and a generated SECRET_KEY
   • terminates HTTPS at its proxy; settings.py trusts X-Forwarded-Proto
   • RENDER_EXTERNAL_HOSTNAME auto-added to ALLOWED_HOSTS / CSRF origins
```

- **Static files** (CSS/JS/images) are served by **WhiteNoise** from the app process —
  no separate CDN or storage bucket needed.
- **Uploaded media** (admin-uploaded creator/team/banner images) are served by Django;
  in `DEBUG` via the dev static helper, in production via a small `serve` route. Note:
  the committed demo images work everywhere, but *new* uploads to a host's local disk
  are ephemeral — for durable uploads, switch to object storage (S3 / R2).

---

## 10. Directory map (what lives where)

```
AdTubers/
├── ARCHITECTURE.md          ← you are here
├── README.md                ← setup, run, and configuration guide
├── Dockerfile               ← production image (gunicorn + WhiteNoise)
├── render.yaml              ← one-click Render deployment blueprint
├── requirements.txt         ← pinned Python dependencies
├── Pipfile                  ← alternative dependency spec (pipenv)
└── tubers/                  ← the Django project root (manage.py lives here)
    ├── manage.py            ← Django's command-line entry point
    ├── db.sqlite3           ← local SQLite database
    ├── tubers/              ← PROJECT config package
    │   ├── settings.py      ← all configuration (env-driven)
    │   ├── urls.py          ← root URL routing → includes each app
    │   ├── wsgi.py / asgi.py← server entry points
    │   └── static/          ← source CSS / JS / image assets
    │
    ├── webpages/            ← marketing pages + Team/Slider + seed_demo
    ├── youtubers/           ← creator catalogue + AI recommender
    ├── hiretubers/          ← booking-request form handler
    ├── accounts/            ← login / register / dashboard
    ├── contactpage/         ← contact-form message store
    ├── contactinfo/         ← site-wide contact details (single row)
    │
    ├── templates/           ← all HTML (shared base + per-app folders)
    │   ├── base.html        ← the master layout every page extends
    │   ├── includes/        ← header, navbar, footer, pagination partials
    │   ├── webpages/        ← home, about, services, contact
    │   ├── youtubers/       ← list, detail, search, recommend
    │   └── accounts/        ← login, register, dashboard, logout
    │
    ├── static/              ← collected/served static assets
    └── media/               ← uploaded images (creators, team, banners)
```

Inside each app you'll find the standard Django files:
`models.py` (tables), `views.py` (request handlers), `urls.py` (routes),
`admin.py` (admin panel config), `apps.py` (app registration), and `migrations/`
(database schema history).

---

## 11. Mini glossary

| Term            | Meaning in this project                                                        |
| --------------- | ------------------------------------------------------------------------------ |
| **App**         | A self-contained Django module owning one feature (e.g. `youtubers`).          |
| **Model**       | A Python class mapped to one database table.                                   |
| **View**        | A Python function that turns a web request into a response.                     |
| **Template**    | An HTML file with `{{ placeholders }}` filled in by a view's context.          |
| **Context**     | The dictionary of data a view hands to a template.                             |
| **Migration**   | An auto-generated file recording a change to the database schema.              |
| **Tuber**       | The project's shorthand for a YouTuber / content creator.                      |
| **Booking**     | A `Hiretuber` row — someone's request to hire a creator.                       |
| **Slider**      | A banner slide on the homepage carousel.                                       |
| **allauth**     | The library that adds optional Google/Facebook social login.                   |

---

*For a running app and setup steps, see [README.md](README.md). Every Python module in
the codebase also carries a docstring describing its specific role.*
