from django import forms
from main.models import StatusUser

class StatusUserForm(forms.ModelForm):
    class Meta:
        model = StatusUser()
        fields = ['text']