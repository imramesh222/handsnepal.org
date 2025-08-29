from django.urls import path
from . import admin_views
from .dashboard_views import (
    admin_notice_list, admin_add_notice, admin_edit_notice, admin_delete_notice,
    admin_career_list, admin_add_career, admin_edit_career, admin_delete_career,
    admin_career_application_list, mark_application_viewed
)

urlpatterns = [
    # Dashboard
    path('', admin_views.dashboard_home, name='dashboard_home'),

    # Homepage Section
    path('carousel/', admin_views.carouselitem_list, name='carouselitem_list'),
    path('carousel/add/', admin_views.add_carouselitem, name='add_carouselitem'),
    path('carousel/edit/<int:pk>/', admin_views.edit_carouselitem, name='edit_carouselitem'),
    path('carousel/delete/<int:pk>/', admin_views.delete_carouselitem, name='delete_carouselitem'),

    # governance urls
    path('governance/', admin_views.governance_list, name='governance_list'),
    path('governance/add/', admin_views.add_governance, name='add_governance'),
    path('governance/<int:pk>/edit/', admin_views.edit_governance, name='edit_governance'),
    path('governance/<int:pk>/delete/', admin_views.delete_governance, name='delete_governance'),

    path('about-info/edit/', admin_views.aboutinfo_edit, name='aboutinfo_edit'),
    
    
    path('about-images/add/', admin_views.add_aboutimage, name='add_aboutimage'),
    path('about-images/', admin_views.aboutimage_list, name='aboutimage_list'),
    path('about-images/edit/<int:pk>/', admin_views.edit_aboutimage, name='edit_aboutimage'),
    path('about-images/delete/<int:pk>/', admin_views.delete_aboutimage, name='delete_aboutimage'),

    
    path('facts/', admin_views.fact_list, name='fact_list'),
    path('facts/add/', admin_views.add_fact, name='add_fact'),
    path('facts/edit/<int:pk>/', admin_views.edit_fact, name='edit_fact'),
    path('facts/delete/<int:pk>/', admin_views.delete_fact, name='delete_fact'),

    # FeatureImage URLs
    path('feature-images/', admin_views.featureimage_list, name='featureimage_list'),
    path('feature-images/add/', admin_views.add_featureimage, name='add_featureimage'),
    path('feature-images/edit/<int:pk>/', admin_views.edit_featureimage, name='edit_featureimage'),
    path('feature-images/delete/<int:pk>/', admin_views.delete_featureimage, name='delete_featureimage'),

    # Feature URLs
    path('features/', admin_views.feature_list, name='feature_list'),
    path('features/add/', admin_views.add_feature, name='add_feature'),
    path('features/edit/<int:pk>/', admin_views.edit_feature, name='edit_feature'),
    path('features/delete/<int:pk>/', admin_views.delete_feature, name='delete_feature'),


    path('services/', admin_views.service_list, name='service_list'),
    path('services/add/', admin_views.add_service, name='add_service'),
    path('services/edit/<int:pk>/', admin_views.edit_service, name='edit_service'),
    path('services/delete/<int:pk>/', admin_views.delete_service, name='delete_service'),

    
    path('projects/', admin_views.project_list, name='project_list'),
    path('projects/add/', admin_views.add_project, name='add_project'),
    path('projects/edit/<int:pk>/', admin_views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', admin_views.delete_project, name='delete_project'),


    path('team/', admin_views.team_list, name='team_list'),
    path('team/add/', admin_views.add_team_member, name='add_team_member'),
    path('team/edit/<int:pk>/', admin_views.edit_team_member, name='edit_team_member'),
    path('team/delete/<int:pk>/', admin_views.delete_team_member, name='delete_team_member'),


    path('testimonials/', admin_views.testimonial_list, name='testimonial_list'),
    path('testimonials/add/', admin_views.add_testimonial, name='add_testimonial'),
    path('testimonials/edit/<int:pk>/', admin_views.edit_testimonial, name='edit_testimonial'),
    path('testimonials/delete/<int:pk>/', admin_views.delete_testimonial, name='delete_testimonial'),

    # CONTACT INFO
    path('contact-info/', admin_views.contactinfo_list, name='contactinfo_list'),
    path('contact-info/add/', admin_views.add_contactinfo, name='add_contactinfo'),
    path('contact-info/edit/<int:pk>/', admin_views.edit_contactinfo, name='edit_contactinfo'),
    path('contact-info/delete/<int:pk>/', admin_views.delete_contactinfo, name='delete_contactinfo'),

    # CONTACT MESSAGES
    path('contact-messages/', admin_views.contactmessage_list, name='contactmessage_list'),
    path('contact-messages/delete/<int:pk>/', admin_views.delete_contactmessage, name='delete_contactmessage'),

    # Downloads
    path('downloads/', admin_views.download_list, name='download_list'),
    path('downloads/add/', admin_views.add_download, name='add_download'),
    path('downloads/edit/<int:pk>/', admin_views.edit_download, name='edit_download'),
    path('downloads/delete/<int:pk>/', admin_views.delete_download, name='delete_download'),

    # Reports
    path('reports/', admin_views.report_list, name='report_list'),
    path('reports/add/', admin_views.add_report, name='add_report'),
    path('reports/edit/<int:pk>/', admin_views.edit_report, name='edit_report'),
    path('reports/delete/<int:pk>/', admin_views.delete_report, name='delete_report'),

    # Notices
    path('admin_notices/', admin_notice_list, name='admin_notice_list'),
    path('admin_notices/add/', admin_add_notice, name='admin_add_notice'),
    path('admin_notices/edit/<int:pk>/', admin_edit_notice, name='admin_edit_notice'),
    path('admin_notices/delete/<int:pk>/', admin_delete_notice, name='admin_delete_notice'),

    # Career Management
    path('careers/', admin_career_list, name='admin_career_list'),
    path('careers/add/', admin_add_career, name='admin_add_career'),
    path('careers/edit/<int:pk>/', admin_edit_career, name='admin_edit_career'),
    path('careers/delete/<int:pk>/', admin_delete_career, name='admin_delete_career'),
    path('careers/applications/', admin_career_application_list, name='admin_career_application_list'),
    path('careers/applications/<int:pk>/mark-viewed/', mark_application_viewed, name='mark_application_viewed'),

    # CLIENTS
    path('clients/', admin_views.client_list, name='client_list'),
    path('clients/add/', admin_views.admin_add_client, name='add_client'),
    path('clients/edit/<int:pk>/', admin_views.admin_edit_client, name='edit_client'),
    path('clients/delete/<int:pk>/', admin_views.admin_delete_client, name='delete_client'),

    # NEWSLETTER
    path('newsletter/', admin_views.newsletter_list, name='newsletter_list'),
    path('newsletter/delete/<int:pk>/', admin_views.delete_newsletter_subscriber, name='delete_newsletter_subscriber'),
    path('newsletter-subscribers/export-csv/', admin_views.export_newsletter_subscribers_csv, name='export_newsletter_subscribers_csv'),

    # ORGANIZATION DETAILS
    path('organizationdetails/', admin_views.organizationdetail_list, name='organizationdetail_list'),
    path('organizationdetails/add/', admin_views.add_organizationdetail, name='add_organizationdetail'),
    path('organizationdetails/<int:pk>/edit/', admin_views.edit_organizationdetail, name='edit_organizationdetail'),
    path('organizationdetails/<int:pk>/delete/', admin_views.delete_organizationdetail, name='delete_organizationdetail'),

    #Photo
    path('photos/', admin_views.photo_list, name='photo_list'),
    path('photos/add/', admin_views.add_photo, name='add_photo'),
    path('photos/edit/<int:pk>/', admin_views.edit_photo, name='edit_photo'),
    path('photos/delete/<int:pk>/', admin_views.delete_photo, name='delete_photo'),

    #Video
    path('videos/', admin_views.video_list, name='video_list'),
    path('videos/add/', admin_views.add_video, name='add_video'),
    path('videos/edit/<int:pk>/', admin_views.edit_video, name='edit_video'),
    path('videos/delete/<int:pk>/', admin_views.delete_video, name='delete_video'),
    
    path('keyinfo/', admin_views.key_info_view, name='key_info'),
    path('organization-content/edit/', admin_views.edit_organization_content, name='edit_organization_content'),



]
