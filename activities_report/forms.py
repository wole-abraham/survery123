from django import forms
from .models import Activities, ActivityPhoto, ActivityVideo
from .choices import machines, activitiess


class Survey(forms.ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'
        widgets = {
            'date_of_activity': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    activity_type = forms.ChoiceField(choices=activitiess, required=True)

class ActivityPhotoForm(forms.ModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ['image']

class ActivityVideoForm(forms.ModelForm):
    class Meta:
        model = ActivityVideo
        fields = ['video']