# hello_world Stuff
from hello_world.base.emails import SendTransactionalEmail
from hello_world.users.auth.tokens import get_token_for_password_reset


class SendPasswordResetEmail(SendTransactionalEmail):
    TEMPLATE = "emails/users/auth/password_reset_mail.tpl"
    SUBJECT = "Reset your Password!"
    EMAIL_ENABLED = True

    def __init__(self, user):
        self.user = user

    def get_context(self):
        return {"user": self.user, "token": get_token_for_password_reset(self.user)}

    def get_to_emails(self):
        return [self.user.email]
