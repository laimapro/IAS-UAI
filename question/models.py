from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

from project.models import Project


class Category(models.Model):
    title = models.CharField(_('Title'), max_length=145)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    category = models.ForeignKey(Category, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.title


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(_('Text'), max_length=255)
    feedback = models.TextField(_('Feedback'), blank=True, null=True)
    correct = models.BooleanField(_('Correct'), default=False)

    class Meta:
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

    def __str__(self):
        return self.text
