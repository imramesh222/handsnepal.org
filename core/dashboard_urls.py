from django.urls import path
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    # Notice Management
    path('notices/', dashboard_views.admin_notice_list, name='admin_notice_list'),
    path('notices/add/', dashboard_views.admin_add_notice, name='admin_add_notice'),
    path('notices/edit/<int:pk>/', dashboard_views.admin_edit_notice, name='admin_edit_notice'),
    path('notices/delete/<int:pk>/', dashboard_views.admin_delete_notice, name='admin_delete_notice'),
    
    # Career Management
    path('careers/', dashboard_views.admin_career_list, name='admin_career_list'),
    path('careers/add/', dashboard_views.admin_add_career, name='admin_add_career'),
    path('careers/edit/<int:pk>/', dashboard_views.admin_edit_career, name='admin_edit_career'),
    path('careers/delete/<int:pk>/', dashboard_views.admin_delete_career, name='admin_delete_career'),
    path('careers/applications/', dashboard_views.admin_career_application_list, name='admin_career_application_list'),
    path('careers/applications/<int:pk>/mark-viewed/', dashboard_views.mark_application_viewed, name='mark_application_viewed'),
]
