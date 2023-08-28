# Third Party Stuff
from django.conf import settings
from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class SendTransactionalEmail(object):
    TEMPLATE = None
    SUBJECT = ""
    EMAIL_ENABLED = False

    def get_to_emails(self):
        raise NotImplementedError("This method needs to be implemented")

    def get_cc_emails(self):
        return None

    def get_group_id(self):
        return None

    def get_context(self):
        raise NotImplementedError("Email Context not provided")

    def get_email_subject(self, ctx):
        if not self.SUBJECT:
            raise NotImplementedError("Email Subject not provided")
        return self.SUBJECT

    def get_template(self):
        if not self.TEMPLATE:
            raise NotImplementedError("Email Template not provided")
        return self.TEMPLATE

    def is_email_enabled(self):
        return self.EMAIL_ENABLED

    def get_connection(self):
        return get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        )

    def get_from_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def send_email(self):
        ctx = self.get_context()
        template = render_to_string(self.get_template(), ctx)
        if self.is_email_enabled():
            message = EmailMultiAlternatives(
                subject=self.get_email_subject(ctx),
                body=template,
                from_email=self.get_from_email(),
                cc=self.get_cc_emails(),
                to=self.get_to_emails(),
            )
            message.attach_alternative(template, "text/html")
            message.send(fail_silently=False)
