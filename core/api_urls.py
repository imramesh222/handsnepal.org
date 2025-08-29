from django.urls import path
from .api_views import (
    NoticeListAPIView, NoticeDetailAPIView,
    CareerListAPIView, CareerDetailAPIView
)

urlpatterns = [
    # Notice endpoints
    path('notices/', NoticeListAPIView.as_view(), name='notice-list'),
    path('notices/<int:pk>/', NoticeDetailAPIView.as_view(), name='notice-detail'),
    
    # Career endpoints
    path('careers/', CareerListAPIView.as_view(), name='career-list'),
    path('careers/<int:pk>/', CareerDetailAPIView.as_view(), name='career-detail'),
]
