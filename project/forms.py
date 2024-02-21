import uuid

from django import forms


class InvitationForm(forms.Form):
    email = forms.EmailField()
    project_id = forms.UUIDField(initial=uuid.uuid4(), widget=forms.HiddenInput)
    project_type = forms.IntegerField(widget=forms.HiddenInput)


class ParticipantInvitationForm(forms.Form):
    email = forms.EmailField()
    project_id = forms.UUIDField(initial=uuid.uuid4(), widget=forms.HiddenInput)