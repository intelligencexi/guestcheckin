from django.urls import path
from . import views
from .views import GuestUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('list_guests/', views.list_guests, name='list_guests'),
    path('guest/<int:pk>/edit/', GuestUpdateView.as_view(), name='guest-edit'),
]
