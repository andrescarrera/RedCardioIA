# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from examples import views

urlpatterns = [

    # The examples page
    path('', views.index, name='examples'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
