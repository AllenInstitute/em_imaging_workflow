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
from at_em_imaging_workflow.views import chunk_view, page_satchel
admin.autodiscover()

urlpatterns = [
    url(r'^workflow_engine/', include('workflow_engine.urls')),
    url(r'^development/', include('development.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^at_em/chunks', chunk_view.chunks_page, name='chunks'),
    url(r'^at_em/page_satchel', page_satchel.page_satchel, name='page_satchel')
]
