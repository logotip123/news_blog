from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.get_registration, name='registration'),
    path('login', views.get_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('confirm/<uuid>', views.user_confirm, name='confirm'),
]
