from django.db import models
from django.core.mail import send_mail
from tinymce.models import HTMLField
from django.template.loader import render_to_string
from django.conf import settings


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=125)
    phone = models.CharField(max_length=25)
    message = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' (' + self.email + ')'

    def save(self, *args, **kwargs):
        super(Contact, self).save(*args, **kwargs)

        data = {'obj': self}
        msg_txt = render_to_string('dashboard/emails/msg.txt', data)
        msg_html = render_to_string('dashboard/emails/msg.html', data)

        send_mail(
            'Contact us',
            msg_txt,
            "IAS <%s>" % settings.EMAIL_HOST_USER,
            [self.email, settings.EMAIL_HOST_USER],
            fail_silently=True,
            html_message=msg_html,
        )


class Language(models.Model):
    title = models.CharField(max_length=125)
    short = models.CharField(max_length=10)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title + ' - ' + self.short
