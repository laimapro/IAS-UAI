from django.db import models
from project.models import Project
from django.utils.translation import gettext_lazy as _
import uuid

from question.models import Question, Option
from users.models import Participant


class Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instance_project = models.ForeignKey(Project, related_name='instances', on_delete=models.CASCADE,
                                         verbose_name=_('Project'))
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Generating situation'), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Instance')
        verbose_name_plural = _('Instances')

    def __str__(self):
        return self.title


class QuestionInstance(models.Model):
    question_pj = models.ForeignKey(Question, related_name='questions_pj', on_delete=models.CASCADE)
    instance_pj = models.ForeignKey(Instance, related_name='questions', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Question Instance')
        verbose_name_plural = _('Question Instances')

    def __str__(self):
        return self.question_pj.title


class InstanceAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(Participant, related_name='users_answer', on_delete=models.CASCADE, verbose_name=_('User'))
    instance_id = models.ForeignKey(Instance, related_name='instances_answer', on_delete=models.CASCADE, verbose_name=_('Instance'))
    status_attempt = models.IntegerField(_('Status Attempt'), default=0)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Instance Attempt')
        verbose_name_plural = _('Instance Attempts')

    def __str__(self):
        return self.instance_id.title


class InstanceAttemptAnswer(models.Model):
    LIKERT_CHOICES = [
        (1, '1'),(2, '2'),(3, '3'),(4, '4'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10'),
    ]
    question_id = models.ForeignKey(Question, related_name='questions_answer', on_delete=models.CASCADE, verbose_name=_('Question'))
    option_id = models.ForeignKey(Option, related_name='options_answer', on_delete=models.CASCADE, verbose_name=_('Option'))
    instance_attempt_id = models.ForeignKey(InstanceAttempt, related_name='instances_attempt_answer', on_delete=models.CASCADE, verbose_name=_('Instance Attempt'))
    likert_scale = models.IntegerField(_('Likert scale'), choices=LIKERT_CHOICES, default=1, blank=True, null=True)
    attempt_number = models.IntegerField(_('Attempt number'), default=1)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Instance Attempt Answer')
        verbose_name_plural = _('Instance Attempt Answers')

    def __str__(self):
        return self.question_id.title
