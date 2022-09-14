from django.urls import path
from streamapp import views


urlpatterns = [
    path('videostream/<int:pk>/<int:count>/', views.index, name='VideoStreaming'),
    ]

 