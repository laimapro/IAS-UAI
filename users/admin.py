from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Manager, Participant, Country, Coordinator

# admin.site.register(Country)
# admin.site.register(Manager)


class ParticipantAdmin(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('name', 'email', 'pj')


class ManagerAdmin(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('name', 'email')


class CoordinatorAdmin(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('name', 'email')


admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.register(Manager, ManagerAdmin)


@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Custom fields", {"fields": ("type", "name", "language")}),
    )
