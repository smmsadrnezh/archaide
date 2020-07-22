from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('register/', views.register, name='register'),


]
