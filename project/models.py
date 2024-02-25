from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Coordinator, Manager
import uuid
import random


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

    def save(self, *args, **kwargs):
        # Verifica se o objeto é novo (não tem um ID)
        if not self.pk:
            # Gera um número de 6 dígitos para o campo pj_code
            self.pj_code = self.generate_project_code()
        super().save(*args, **kwargs)

    def generate_project_code(self):
        # Gera um número aleatório de 6 dígitos
        return random.randint(100000, 999999)
