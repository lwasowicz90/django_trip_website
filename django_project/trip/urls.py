from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='trip-home'),
    path('about/', views.about, name='trip-about'),

]

