from django.urls import path, include, re_path
from QlChungCu import views
from rest_framework import routers


r = routers.DefaultRouter()
r.register('People', views.PeopleViewSet)

urlpatterns = [
    path('', include(r.urls)),
]