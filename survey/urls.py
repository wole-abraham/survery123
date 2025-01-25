"""
URL configuration for survey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from activities_report.views import page, submitted, view_report, get_activity

from rest_framework.routers import DefaultRouter
from activities_report.views import ActivityViewSet, ActivityPhotoViewSet, ActivityVideoViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet)
router.register(r'activities/(?P<activity_id>\d+)/photos', ActivityPhotoViewSet)
router.register(r'activities/(?P<activity_id>\d+)/videos', ActivityVideoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitted/', submitted, name='submitted'),
    path('report/', view_report, name='report'),
    path('', page, name='page'),
    path('api/', include(router.urls)),
    path('get-activities/<str:category>', get_activity, name='get-activity')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)