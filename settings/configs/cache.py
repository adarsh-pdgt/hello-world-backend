from settings.configs.knox import *

# Caches
CACHE_NAMES = {
    "AUTH_TOKEN_EXPIRY_CACHE": {
        "key": "auth-token-{pk}-expiry",
        "timeout": REST_KNOX["MIN_REFRESH_INTERVAL"],
    },
    "USER_LAST_ACTIVE_CACHE": {
        "key": "user-last-active-{user_id}-timestamp",
        "timeout": USER_LAST_ACTIVE_UPDATE_THRESHOLD,
    },
}
