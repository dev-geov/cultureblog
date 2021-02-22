from django.core.mail import send_mail
from django.conf import settings


class Email:

    def __init__(self, subject, message, receiver=None):
        self._subject = subject
        self._message = message
        self._receivers = [receiver, settings.EMAIL_HOST_USER]
    

    def send(self):

        mail = send_mail(
            subject=self._subject,
            message=self._message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=self._receiver,
        )

        if mail:
            return True
        return False