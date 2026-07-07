"""Models for the ``accounts`` app.

This app deliberately has no models of its own — it reuses Django's built-in
``django.contrib.auth.models.User`` for accounts. It exists only to provide the
custom login/register/logout/dashboard views.
"""

from django.db import models  # noqa: F401 (kept for future models)
