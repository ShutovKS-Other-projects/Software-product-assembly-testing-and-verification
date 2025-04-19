from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ssd/<int:pk>/', views.SSDDetailView.as_view(), name='ssd_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
]
