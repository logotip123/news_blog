from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_index, name='index'),
    path('post/<slug>', views.get_post, name='post'),
    path('add/', views.add_post, name='add_post'),
]
