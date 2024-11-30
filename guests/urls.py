from django.urls import path
from . import views
from .views import GuestUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    path('add_guest/', views.add_guest, name='add_guest'),
    path('modal/open/', views.open_modal, name='open_modal'),
    path('modal/close/', views.close_modal, name='close_modal'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('list_guests/', views.list_guests, name='list_guests'),
    path('search/', views.search, name="search"),
    path('guest/<int:pk>/edit/', GuestUpdateView.as_view(), name='guest-edit'),
]
