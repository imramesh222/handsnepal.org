from django.urls import path
from . import views
from .api_views import (
    NoticeListAPIView, TeamListAPIView, TeamDetailAPIView,
    CareerListAPIView, CareerDetailAPIView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('governance/', views.governance_view, name='governance'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('projects/', views.projects, name='projects'),
    path('reports/', views.reports, name='reports'),
    path('downloads/', views.downloads, name='downloads'),
    path('notice/', views.notice, name='notice_list'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('contact/', views.contact, name='contact'),
    path('clients/', views.clients, name='clients'),
    path('photo/', views.photo, name='photo'),
    path('video/', views.video, name='video'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('key/info/', views.key_info_view, name='key_info_view'),
    
    # API Endpoints
    path('api/notices/', NoticeListAPIView.as_view(), name='api_notices'),
    
    # Team URLs
    path('team/', views.team_list, name='team_list'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
    path('team/add/', views.team_create, name='team_create'),
    path('team/<int:pk>/edit/', views.team_update, name='team_update'),
    path('team/<int:pk>/delete/', views.team_delete, name='team_delete'),
    
    # Team API Endpoints
    path('api/teams/', TeamListAPIView.as_view(), name='api_teams'),
    path('api/teams/<int:pk>/', TeamDetailAPIView.as_view(), name='api_team_detail'),
    
    # Career URLs
    path('careers/', views.CareerListView.as_view(), name='career_list'),
    path('careers/<int:pk>/', views.CareerDetailView.as_view(), name='career_detail'),
    path('careers/add/', views.CareerCreateView.as_view(), name='career_create'),
    path('careers/<int:pk>/edit/', views.CareerUpdateView.as_view(), name='career_update'),
    path('careers/<int:pk>/delete/', views.career_delete, name='career_delete'),
    path('careers/<int:pk>/apply/', views.career_apply, name='career_apply'),
    
    # Career API Endpoints
    path('api/careers/', CareerListAPIView.as_view(), name='api_careers'),
    path('api/careers/<int:pk>/', CareerDetailAPIView.as_view(), name='api_career_detail'),
]
