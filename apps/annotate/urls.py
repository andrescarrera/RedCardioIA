from django.urls import path
from annotate import views


urlpatterns = [
    path('paint/<int:pk>/<int:count>/', views.paint, name='paint'),
    path('anotaciones/<int:pk>/<int:id>/', views.list_anot, name='ListAnnotations'),
    ]
