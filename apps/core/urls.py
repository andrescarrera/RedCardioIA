# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [

    path('admin/', admin.site.urls),          # Django admin route
    path("", include("authentication.urls")), # Auth routes - login / register
    path("", include("patients.urls")),             # UI Kits Html files
    
    path("ejemplos/", include("examples.urls")), # Ejemplos plantilla
    
    path("registro_clinico", include("clinical_register.urls")),
    
    path("ver_archivos/", include("viewfiles.urls")),

    path('annotate/', include('annotate.urls')),
    path('streamapp/', include('streamapp.urls')),

     # UI Kits Html files
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)