"""
becoapp URL Configuration

"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^', include('applications.accounts.urls')),
    url(r'^admin/', admin.site.urls),
]
