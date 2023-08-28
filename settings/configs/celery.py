# Third Party Stuff
import environ

env = environ.Env()

# DJANGO CELERY CONFIGURATION
# -----------------------------------------------------------------------------
# see: http://celery.readthedocs.org/en/latest/userguide/tasks.html#task-states
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = env(
    "CELERY_TIMEZONE", default="UTC"
)  # Use Django's timezone by default

CELERY_BEAT_SCHEDULE = {}
