# Standard Library
import logging

# Third Party Stuff
from post_request_task.task import shared_task

# Hello World Stuff
from hello_world.users.auth.emails import SendPasswordResetEmail
from hello_world.users.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_password_reset_mail_task(user_id):
    user = User.objects.filter(id=user_id).first()

    if not user:
        logger.info("Could not send password reset email for user_id=%s", user_id)

    return SendPasswordResetEmail(user).send_email()
