# services/urls.py
from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("", views.service_list, name="service_list"),              # all services + search
    path("<int:pk>/", views.service_detail, name="service_detail"), # service detail
    path("add/", views.add_service, name="add_service"),            # add new service (provider only)
    path("my/", views.my_services, name="my_services"),             # provider’s own services
    path("<int:pk>/edit/", views.edit_service, name="edit_service"),   # ✅ edit
    path("<int:pk>/delete/", views.delete_service, name="delete_service"), # ✅ delete
]
