# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from clinical_register import views

urlpatterns = [

    # The examples page
    path('', views.clinical_register_view, name='clinicalRegisterView'),

]
