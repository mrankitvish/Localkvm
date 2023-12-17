from django.urls import path
from . import views
urlpatterns = [
    path('vmlist/', views.list_vms),
    path('vmdel/<int:vm_id>/', views.delete_vm),
    path('vmadd/', views.create_vm),
]
