from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('submission/<int:task_id>/',views.submission, name="submission"),
    path('submission/result/', views.result, name="result")
]
