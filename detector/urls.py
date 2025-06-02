from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index),
    path('detect/', views.detect, name='detect'),

    path('about/', views.about_view, name='about'),
    path('about.html', views.about_view),
    # path('detect/', DetectView.as_view(), name='detect'),

]