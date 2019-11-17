from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views


urlpatterns = [
    url(r'^/cart/$', views.CartsView.as_view()),
]