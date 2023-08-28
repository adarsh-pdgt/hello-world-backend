# Third Party Stuff
import environ
from datetime import timedelta


env = environ.Env()

# Knox: https://james1345.github.io/django-rest-knox/settings/
# ------------------------------------------------------------------------------
REST_KNOX = {
    "AUTO_REFRESH": True,
    "MIN_REFRESH_INTERVAL": 12 * 60 * 60,  # 12 hour
    "TOKEN_TTL": timedelta(
        minutes=env.int("KNOX_TOKEN_TTL_MINUTES", default=30 * 24 * 60)
    ),  # 30 days
}

# User Last Active Update Threshold
# ------------------------------------------------------------------------------
USER_LAST_ACTIVE_UPDATE_THRESHOLD = 10 * 60  # Threshold in seconds (10 minutes)
