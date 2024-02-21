from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Instance, QuestionInstance, InstanceAttempt, InstanceAttemptAnswer


class InstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'instance_project')
    list_filter = ('instance_project', )


class QuestionInstanceAdmin(admin.ModelAdmin):
    list_display = ('question_pj', 'instance_pj', )


class InstanceAttemptAdmin(admin.ModelAdmin):
    list_display = ('instance_id', 'user_id', 'status_attempt', 'created_at',)


class InstanceAttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'option_id', 'get_instance_title', 'likert_scale', 'attempt_number', 'created_at',)

    def get_instance_title(self, obj):
        return obj.instance_attempt_id.instance_id.title

    get_instance_title.short_description = _('Instance')


admin.site.register(Instance, InstanceAdmin)
admin.site.register(QuestionInstance, QuestionInstanceAdmin)
admin.site.register(InstanceAttempt, InstanceAttemptAdmin)
admin.site.register(InstanceAttemptAnswer, InstanceAttemptAnswerAdmin)
