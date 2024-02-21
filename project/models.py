from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Coordinator, Manager
import uuid


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pj_name = models.CharField(_('Project name'), max_length=255)
    pj_code = models.PositiveIntegerField(_('Project code'), unique=True)
    pj_description = models.TextField(_('Description'), max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coordinator = models.ForeignKey(Coordinator, verbose_name=_('Coordinator'), null=True, blank=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey(Manager, verbose_name=_('Manager'), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-pk']

    def __str__(self):
        return self.pj_name
