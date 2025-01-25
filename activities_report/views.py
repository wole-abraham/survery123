from django.shortcuts import render, redirect
from .forms import Survey, ActivityPhotoForm, ActivityVideoForm
from .models import Activities, ActivityPhoto, ActivityVideo
from django.http import HttpResponse
from .choices import activities, project_section
from django.http import JsonResponse

def page(request):

    if request.method == 'POST':
        survey_form = Survey(request.POST)
        if survey_form.is_valid():
            # Save the activity
            activity = survey_form.save()

            # Handle photo uploads
            for file in request.FILES.getlist('photos'):
                ActivityPhoto.objects.create(activity=activity, image=file)

            # Handle video uploads
            for file in request.FILES.getlist('videos'):
                ActivityVideo.objects.create(activity=activity, video=file)

            return redirect('submitted')  # Replace with your desired success URL
        else:
            print(survey_form.errors)

    else:
        survey_form = Survey()

    return render(request, 'survey/form.html', {
        'form': survey_form,
    })

def get_activity(request, category):
    activities_list = activities.get(category)
    return JsonResponse({'activities': activities_list})

def get_section(request, project):
    project_list = project_section.get(project)
    return JsonResponse({'projects': project_list})


def submitted(request):
    return render(request, 'survey/submitted.html')

def view_report(request):
    activities = Activities.objects.all()
    return render(request, 'survey/view_reports.html', context={'activities': activities})


# API

from rest_framework import viewsets
from .serializers import ActivitySerializer, ActivityPhotoSerializer, ActivityVideoSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activities.objects.all()
    serializer_class = ActivitySerializer

class ActivityPhotoViewSet(viewsets.ModelViewSet):
    queryset = ActivityPhoto.objects.all()
    serializer_class = ActivityPhotoSerializer

    def perform_create(self, serializer):
        activity = Activities.objects.get(id=self.kwargs['activity_id'])
        serializer.save(activity=activity)

class ActivityVideoViewSet(viewsets.ModelViewSet):
    queryset = ActivityVideo.objects.all()
    serializer_class = ActivityVideoSerializer

    def perform_create(self, serializer):
        activity = Activities.objects.get(id=self.kwargs['activity_id'])
        serializer.save(activity=activity)