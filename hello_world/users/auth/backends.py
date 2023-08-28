# Third Party Stuff
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from knox.settings import knox_settings

# Hello World Stuff
from hello_world.users.auth.tasks import save_expiry_for_auth_token, set_user_last_active

AUTH_TOKEN_CACHE_DETAILS = settings.CACHE_NAMES["AUTH_TOKEN_EXPIRY_CACHE"]
USER_LAST_ACTIVE_CACHE_DETAILS = settings.CACHE_NAMES["USER_LAST_ACTIVE_CACHE"]


class KnoxTokenLastActiveBackend(KnoxTokenAuthentication):
    def authenticate(self, request):
        data = super(KnoxTokenLastActiveBackend, self).authenticate(request)
        if data:
            user = data[0]
            if user and user.is_authenticated:
                self.update_user_last_active_timestamp(user)

        return data

    def renew_token(self, auth_token):
        # We need to first fetch the expiry from cache because the when we save the value to db then
        # transaction makes the api calls slow as same user hits multiple api calls on page load. With cache
        # we save all the wait time from transactions
        current_expiry = self.get_expiry_for_token(auth_token)
        new_expiry = timezone.now() + knox_settings.TOKEN_TTL

        # Throttle refreshing of token to avoid db writes
        delta = (new_expiry - current_expiry).total_seconds()
        if delta > knox_settings.MIN_REFRESH_INTERVAL:
            key = AUTH_TOKEN_CACHE_DETAILS["key"].format(pk=auth_token.pk)
            timeout = AUTH_TOKEN_CACHE_DETAILS["timeout"]
            cache.set(key, new_expiry, timeout)
            save_expiry_for_auth_token.apply_async([auth_token.pk, new_expiry])

    def update_user_last_active_timestamp(self, user):
        key = USER_LAST_ACTIVE_CACHE_DETAILS["key"].format(user_id=str(user.id))
        user_last_active = cache.get(key)
        if user_last_active:
            timeout = USER_LAST_ACTIVE_CACHE_DETAILS["timeout"]
            current_time = timezone.now()
            cache.set(key, current_time, timeout)
            set_user_last_active.apply_async([str(user.id), current_time])

    def get_expiry_for_token(self, auth_token):
        # Cache will have the latest expiry
        key = AUTH_TOKEN_CACHE_DETAILS["key"].format(pk=auth_token.pk)
        expiry = cache.get(key)
        return expiry or auth_token.expiry
