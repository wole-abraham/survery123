from django import forms
from .models import Activities, ActivityPhoto, ActivityVideo
from .choices import machines


class Survey(forms.ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'
        widgets = {
            'date_of_activity': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }


class ActivityPhotoForm(forms.ModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ['image']

class ActivityVideoForm(forms.ModelForm):
    class Meta:
        model = ActivityVideo
        fields = ['video']