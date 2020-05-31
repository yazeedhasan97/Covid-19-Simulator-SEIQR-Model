from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    path(r'', views.home),
    # path(r'', views.login),
    # url(r'^S', views.home)
]
