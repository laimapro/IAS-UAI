from django.contrib import admin

from .models import Question, Option, Category


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category', )


class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'feedback', 'correct')
    list_filter = ('question', )


admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
