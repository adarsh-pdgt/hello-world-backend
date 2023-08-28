# Third Party Stuff
from knox.models import AuthToken
from post_request_task.task import shared_task

# Hello World Stuff Stuff
from hello_world.users.models import User


@shared_task
def save_expiry_for_auth_token(auth_token_pk, expiry):
    # Save auth token on celery after the request has been completed
    AuthToken.objects.filter(pk=auth_token_pk).update(expiry=expiry)


@shared_task
def set_user_last_active(user_id, last_active_time):
    # Save last user access time
    User.objects.filter(id=user_id).update(last_active=last_active_time)
