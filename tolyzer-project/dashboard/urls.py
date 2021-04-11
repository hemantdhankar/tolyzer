from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('submission/<int:task_id>/',views.submission, name="submission"),
    path('submission/result/<int:task_id>', views.result, name="result")
]
