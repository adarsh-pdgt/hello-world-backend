# Third Party Stuff
import environ

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from settings.utils import get_release

env = environ.Env()

RELEASE_VERSION = get_release()

SENTRY_DSN = env("SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT", default="local")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment=SENTRY_ENVIRONMENT,
        release=RELEASE_VERSION,
        send_default_pii=True,  # associate users to errors
    )
