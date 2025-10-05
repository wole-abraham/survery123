from django import forms
from .models import Activities, ActivityPhoto, ActivityVideo
from .choices import activitiess, supervisor, engineers, team_cars, project_sections, machines, sources, party


class Survey(forms.ModelForm):
    class Meta:
        model = Activities
        exclude = ['machines', 'machines_source', 'site_engineer', 'supervisors']  # Exclude JSON fields
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

    # Custom fields for form display (not saved to model directly)
    activity_type = forms.ChoiceField(choices=activitiess, required=False)
    supervisors = forms.ChoiceField(choices=supervisor, required=False)
    site_engineer = forms.ChoiceField(choices=engineers, required=False)
    machines = forms.ChoiceField(choices=machines, required=False)
    machines_source = forms.ChoiceField(choices=sources, required=False)
    team_car = forms.ChoiceField(choices=team_cars, required=False)
    team_car_option = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'no')])
    supervision = forms.ChoiceField(choices=party, required=False)
    # project_section is already included from the model, no need to redefine

class ActivityPhotoForm(forms.ModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ['image']

class ActivityVideoForm(forms.ModelForm):
    class Meta:
        model = ActivityVideo
        fields = ['video']