# services/urls.py
from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.service_list, name="service_list"),           
    path("<int:pk>/", views.service_detail, name="service_detail"),
    path("add/", views.add_service, name="add_service"),        
    path("my/", views.my_services, name="my_services"),            
    path("<int:pk>/edit/", views.edit_service, name="edit_service"),  
    path("<int:pk>/delete/", views.delete_service, name="delete_service"), 
]
