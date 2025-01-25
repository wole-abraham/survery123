from django import forms
from .models import Activities, ActivityPhoto, ActivityVideo
from .choices import machines, activitiess, project_sections


class Survey(forms.ModelForm):
    class Meta:
        model = Activities
        fields = '__all__'
        widgets = {
            'date_of_activity': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',  # Format without seconds
            ),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the input matches the desired format
        self.fields['date_of_activity'].input_formats = ['%Y-%m-%dT%H:%M']

    activity_type = forms.ChoiceField(choices=activitiess, required=True)
    project_section = forms.ChoiceField(choices=project_sections, required=True)

class ActivityPhotoForm(forms.ModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ['image']

class ActivityVideoForm(forms.ModelForm):
    class Meta:
        model = ActivityVideo
        fields = ['video']