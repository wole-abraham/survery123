from django.db import models
from . import choices
# Create your models here.
from datetime import datetime

class Activities(models.Model):

    date_of_activity = models.DateTimeField(default=datetime.now())
    project_name = models.CharField(choices=choices.project_choice, max_length=100)
    fullname = models.CharField(choices=choices.names, max_length=100, null=True)
    role = models.CharField(choices=choices.roles, max_length=100, null=True)
    project_section = models.CharField(choices=choices.project_sections, max_length=100, null=True)
    planned_activity_category = models.CharField(choices=choices.activities_category, max_length=100, default=choices.activities_category[0])
    activity_type = models.CharField(choices=choices.activitiess, max_length=100, null=True)
    comment = models.TextField(null=True)
    chainage = models.CharField(choices=choices.chanage, max_length=100, null=True)
    chainage2 = models.CharField(choices=choices.chanage2, max_length=100, null=True)
    site_engineer = models.JSONField(default=list, null=True)
    supervisors = models.JSONField(default=list, null=True)
    party = models.CharField(choices=choices.party, max_length=100, null=True)
    supervision = models.CharField(choices=choices.party, max_length=100, null=True)
    machines = models.JSONField(default=list, null=True)
    machines_source = models.JSONField(default=list, null=True)
    team_car = models.CharField(choices=choices.team_cars, max_length=50, null=True)
    team_car_option = models.CharField(choices=[('yes', 'Yes'), ('no', 'no')], max_length=10, null=True)
    subcontractor_name = models.CharField(choices=choices.subcontractor_names, max_length=50, null=True)

    def __str__(self):
        return f'{self.project_name} - {self.date_of_activity}'
    
class ActivityPhoto(models.Model):
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f"photo for {self.activity.id} {self.activity.project_name}  - {self.activity.date_of_activity}"

class ActivityVideo(models.Model):
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return f"Video for {self.activity.project_name} - {self.activity.date_of_activity}"