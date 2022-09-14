from django.urls import path
from patients import views

from .views import (
    patient_inactivate_view,
)

#app_name = 'patients'
urlpatterns = [
    # The examples page
    path('', views.patients_list_view, name='patientsListView'),
    path('inactivar/<int:id>/', patient_inactivate_view, name='patientDelete'),
]