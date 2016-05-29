from django.contrib.auth.models import Group
from django import forms
from django.utils.translation import ugettext_lazy as _

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions',)
