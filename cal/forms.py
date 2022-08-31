# cal/forms.py

from django import forms
from cal import models

class CalEventForm(forms.ModelForm):
    class Meta:
        model = models.CalEvent
        fields = [
            'name',
            'date',
            'isAnniv',
            'group',
        ]
        labels = {
            'isAnniv': 'Is Anniversary?'
        }
        widgets = {
            
        }