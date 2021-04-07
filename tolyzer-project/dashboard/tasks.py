from celery import shared_task
from django.shortcuts import render, redirect
import time
from . import views


def process():
    for i in range(30):
        print(i)
        time.sleep(1)
    return True

