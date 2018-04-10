from django.conf.urls import include, url
from django.contrib import admin
from workflow_engine.views import home_view


app_name = 'at_em_imaging_workflow'

urlpatterns = [
    url(r'^$', home_view.index, name='index'),
    url(r'^workflow_engine/', include('workflow_engine.urls')),
    url(r'^admin/', admin.site.urls),
]
