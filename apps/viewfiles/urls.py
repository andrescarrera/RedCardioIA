from django.urls import path
from viewfiles import views

urlpatterns = [
    path('<int:id>/', views.files_view_indx, name='filesView'),
    path('', views.files_view_indx, name='filesView'),
    path('<int:pk>/<int:id>/', views.delete_file, name='delete_file'),
]
