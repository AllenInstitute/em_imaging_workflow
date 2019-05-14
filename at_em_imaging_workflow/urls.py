"""blue_sky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
"""
from django.conf.urls import include, url
from django.contrib import admin
from workflow_engine.views import home_view
from .views import page_satchel
from .views.imaging_q_c_view import ImagingQCView
from .views.create_chunk_view import CreateChunkView
from .views.create_gap_section_view import CreateGapSectionView
from .views.faster_job_grid_view import faster_job_grid

admin.autodiscover()

app_name = 'at_em_imaging_workflow'

urlpatterns = (
    url(r'^$', home_view.index, name='index'),
    url(r'^workflow_engine/', include('workflow_engine.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^at_em/page_satchel', page_satchel.page_satchel, name='page_satchel'),
    url(r'^at_em/reimage$', ImagingQCView.as_view()),
    url(
        r'^at_em/create_chunk$',
        CreateChunkView.as_view(),
        name='create_chunk'
    ),  
    url(
        r'^at_em/create_gap_section$',
        CreateGapSectionView.as_view(),
        name='create_gap_section'
    ),
    url(
        r'^at_em/faster_job_grid$',
        faster_job_grid,
        name='faster_job_grid'
    )
)

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)
