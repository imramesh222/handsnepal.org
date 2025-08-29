from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Photo, Video, KeyInfo
from .forms import PhotoForm, VideoForm, KeyInfoForm
from .models import OrganizationContent
from .forms import OrganizationContentForm,GovernanceForm
from .models import (
    AboutImage, AboutInfo, CarouselItem, Download, Fact,
    Feature, FeatureImage, Notice, Project, Report,
    Service, TeamMember, Testimonial, Client, NewsletterSubscriber,Governance,
    ContactInfo, ContactMessage, OrganizationDetail,Career
)

from .admin_forms import (
    AboutImageForm, AboutInfoForm, CarouselItemForm, DownloadForm, FactForm,
    FeatureForm, FeatureImageForm, NoticeForm, ProjectForm, ReportForm,
    ServiceForm, TeamMemberForm, TestimonialForm, ClientForm, ContactInfoForm,
    OrganizationDetailForm,CareerForm
)



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or unauthorized access.')
    return render(request, 'dashboard/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard
@login_required
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')

# -- -------- Carousel Items -------- --
@login_required
def carouselitem_list(request):
    carouselitems = CarouselItem.objects.all()
    return render(request, 'dashboard/carouselitem_list.html', {'carouselitems': carouselitems})

@login_required
def add_carouselitem(request):
    if CarouselItem.objects.count() >= 2:
        messages.warning(request, "You can only add up to 2 carousel items.")
        return redirect('carouselitem_list')

    if request.method == 'POST':
        form = CarouselItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel item added successfully.')
            return redirect('carouselitem_list')
    else:
        form = CarouselItemForm()

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Carousel Item',
        'cancel_url': reverse('carouselitem_list'),
    })


@login_required
def edit_carouselitem(request, pk):
    item = get_object_or_404(CarouselItem, pk=pk)

    if request.method == 'POST':
        form = CarouselItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel item updated successfully.')
            return redirect('carouselitem_list')
    else:
        form = CarouselItemForm(instance=item)

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Carousel Item',
        'cancel_url': reverse('carouselitem_list'),
    })

@login_required
def delete_carouselitem(request, pk):
    obj = get_object_or_404(CarouselItem, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Carousel Item deleted successfully.')
        return redirect('carouselitem_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('carouselitem_list'),
    })

@login_required
def aboutinfo_edit(request):
    about_info, created = AboutInfo.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = AboutInfoForm(request.POST, request.FILES, instance=about_info)
        if form.is_valid():
            form.save()
            messages.success(request, "About Info updated successfully.")
            return redirect('aboutinfo_edit')
    else:
        form = AboutInfoForm(instance=about_info)

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit About Info',
    })

@login_required
def aboutimage_list(request):
    images = AboutImage.objects.all()
    return render(request, 'dashboard/aboutimage_list.html', {'images': images})

@login_required
def add_aboutimage(request):
    if AboutImage.objects.count() >= 1:
        messages.warning(request, "You can only add up to 1 About images.")
        return redirect('aboutimage_list')

    form = AboutImageForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "About image added successfully.")
        return redirect('aboutimage_list')

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add About Image',
        'cancel_url': reverse('aboutimage_list'),
    })

@login_required
def edit_aboutimage(request, pk):
    image = get_object_or_404(AboutImage, pk=pk)
    form = AboutImageForm(request.POST or None, request.FILES or None, instance=image)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "About image updated successfully.")
        return redirect('aboutimage_list')

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit About Image',
        'cancel_url': reverse('aboutimage_list'),
    })

@login_required
def delete_aboutimage(request, pk):
    image = get_object_or_404(AboutImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, "About image deleted successfully.")
        return redirect('aboutimage_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': image,
        'cancel_url': reverse('aboutimage_list'),
    })

@login_required
def fact_list(request):
    facts = Fact.objects.all()
    return render(request, 'dashboard/fact_list.html', {'facts': facts})

@login_required
def add_fact(request):
    if request.method == 'POST':
        form = FactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fact added successfully.')
            return redirect('fact_list')
    else:
        form = FactForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Fact',
        'cancel_url': reverse('fact_list'),
    })

@login_required
def edit_fact(request, pk):
    fact = get_object_or_404(Fact, pk=pk)
    if request.method == 'POST':
        form = FactForm(request.POST, instance=fact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fact updated successfully.')
            return redirect('fact_list')
    else:
        form = FactForm(instance=fact)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Fact',
        'cancel_url': reverse('fact_list'),
    })

@login_required
def delete_fact(request, pk):
    fact = get_object_or_404(Fact, pk=pk)
    if request.method == 'POST':
        fact.delete()
        messages.success(request, 'Fact deleted successfully.')
        return redirect('fact_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': fact,
        'cancel_url': reverse('fact_list'),
    })

# FeatureImage Views

@login_required
def featureimage_list(request):
    images = FeatureImage.objects.all()
    return render(request, 'dashboard/featureimage_list.html', {'images': images})

@login_required
def add_featureimage(request):
    if FeatureImage.objects.exists():
        messages.warning(request, "Only one Feature Image is allowed. You cannot add more.")
        return redirect('featureimage_list')

    if request.method == 'POST':
        form = FeatureImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature Image added successfully.')
            return redirect('featureimage_list')
    else:
        form = FeatureImageForm()

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Feature Image',
        'cancel_url': reverse('featureimage_list'),
    })

@login_required
def edit_featureimage(request, pk):
    image = get_object_or_404(FeatureImage, pk=pk)
    if request.method == 'POST':
        form = FeatureImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature Image updated successfully.')
            return redirect('featureimage_list')
    else:
        form = FeatureImageForm(instance=image)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Feature Image',
        'cancel_url': reverse('featureimage_list'),
    })

@login_required
def delete_featureimage(request, pk):
    image = get_object_or_404(FeatureImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Feature Image deleted successfully.')
        return redirect('featureimage_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': image,
        'cancel_url': reverse('featureimage_list'),
    })


# Feature Views

@login_required
def feature_list(request):
    features = Feature.objects.all()
    return render(request, 'dashboard/feature_list.html', {'features': features})

@login_required
def add_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature added successfully.')
            return redirect('feature_list')
    else:
        form = FeatureForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Feature',
        'cancel_url': reverse('feature_list'),
    })

@login_required
def edit_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feature updated successfully.')
            return redirect('feature_list')
    else:
        form = FeatureForm(instance=feature)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Feature',
        'cancel_url': reverse('feature_list'),
    })

@login_required
def delete_feature(request, pk):
    feature = get_object_or_404(Feature, pk=pk)
    if request.method == 'POST':
        feature.delete()
        messages.success(request, 'Feature deleted successfully.')
        return redirect('feature_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': feature,
        'cancel_url': reverse('feature_list'),
    })

@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, 'dashboard/service_list.html', {'services': services})

@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service added successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Service',
        'cancel_url': reverse('service_list'),
    })

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Service',
        'cancel_url': reverse('service_list'),
    })

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully.')
        return redirect('service_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': service,
        'cancel_url': reverse('service_list'),
    })

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project added successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Add Project', 'cancel_url': reverse('project_list')})

@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Edit Project', 'cancel_url': reverse('project_list')})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('project_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': project, 'cancel_url': reverse('project_list')})

@login_required
def team_list(request):
    members = TeamMember.objects.all()
    return render(request, 'dashboard/team_list.html', {'members': members})

@login_required
def add_team_member(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully.')
            return redirect('team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Add Team Member', 'cancel_url': reverse('team_list')})

# views.py

@login_required
def governance_list(request):
    governance = Governance.objects.all()
    return render(request, 'dashboard/governance_list.html', {'governance': governance})

@login_required
def add_governance(request):
    if request.method == 'POST':
        form = GovernanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Governance member added successfully.')
            return redirect('governance_list')
    else:
        form = GovernanceForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form, 
        'title': 'Add Governance Member', 
        'cancel_url': reverse('governance_list')
    })

@login_required
def edit_governance(request, pk):
    member = get_object_or_404(Governance, pk=pk)
    if request.method == 'POST':
        form = GovernanceForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Governance member updated successfully.')
            return redirect('governance_list')
    else:
        form = GovernanceForm(instance=member)
    return render(request, 'dashboard/generic_form.html', {
        'form': form, 
        'title': 'Edit Governance Member', 
        'cancel_url': reverse('governance_list')
    })

@login_required
def delete_governance(request, pk):
    member = get_object_or_404(Governance, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Governance member deleted successfully.')
        return redirect('governance_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': member, 
        'cancel_url': reverse('governance_list')
    })



@login_required
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully.')
            return redirect('team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Edit Team Member', 'cancel_url': reverse('team_list')})

@login_required
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted successfully.')
        return redirect('team_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': member, 'cancel_url': reverse('team_list')})

@login_required
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonial_list.html', {'testimonials': testimonials})

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully.')
            return redirect('testimonial_list')
    else:
        form = TestimonialForm()
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Add Testimonial', 'cancel_url': reverse('testimonial_list')})

@login_required
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully.')
            return redirect('testimonial_list')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'dashboard/generic_form.html', {'form': form, 'title': 'Edit Testimonial', 'cancel_url': reverse('testimonial_list')})

@login_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully.')
        return redirect('testimonial_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': testimonial, 'cancel_url': reverse('testimonial_list')})

# CONTACT INFO

@login_required
def contactinfo_list(request):
    infos = ContactInfo.objects.all()
    return render(request, 'dashboard/contactinfo_list.html', {'infos': infos})

@login_required
def add_contactinfo(request):
    if ContactInfo.objects.exists():
        messages.warning(request, "Only one Contact Info is allowed.")
        return redirect('contactinfo_list')

    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact info saved successfully.')
            return redirect('contactinfo_list')
    else:
        form = ContactInfoForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Contact Info',
        'cancel_url': reverse('contactinfo_list'),
    })

@login_required
def edit_contactinfo(request, pk):
    info = get_object_or_404(ContactInfo, pk=pk)
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact info updated.')
            return redirect('contactinfo_list')
    else:
        form = ContactInfoForm(instance=info)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Contact Info',
        'cancel_url': reverse('contactinfo_list'),
    })

@login_required
def delete_contactinfo(request, pk):
    info = get_object_or_404(ContactInfo, pk=pk)
    if request.method == 'POST':
        info.delete()
        messages.success(request, 'Contact info deleted.')
        return redirect('contactinfo_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': info,
        'cancel_url': reverse('contactinfo_list'),
    })


# CONTACT MESSAGES (read-only list + delete)

@login_required
def contactmessage_list(request):
    messages_list = ContactMessage.objects.order_by('-created_at')
    return render(request, 'dashboard/contactmessage_list.html', {'messages_list': messages_list})

@login_required
def delete_contactmessage(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
        return redirect('contactmessage_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': msg,
        'cancel_url': reverse('contactmessage_list'),
    })

# Downloads

@login_required
def download_list(request):
    downloads = Download.objects.all()
    return render(request, 'dashboard/download_list.html', {'downloads': downloads})

@login_required
def add_download(request):
    if request.method == 'POST':
        form = DownloadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Download added successfully.')
            return redirect('download_list')
    else:
        form = DownloadForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Download',
        'cancel_url': reverse('download_list'),
    })

@login_required
def edit_download(request, pk):
    download = get_object_or_404(Download, pk=pk)
    if request.method == 'POST':
        form = DownloadForm(request.POST, request.FILES, instance=download)
        if form.is_valid():
            form.save()
            messages.success(request, 'Download updated successfully.')
            return redirect('download_list')
    else:
        form = DownloadForm(instance=download)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Download',
        'cancel_url': reverse('download_list'),
    })

@login_required
def delete_download(request, pk):
    download = get_object_or_404(Download, pk=pk)
    if request.method == 'POST':
        download.delete()
        messages.success(request, 'Download deleted successfully.')
        return redirect('download_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': download,
        'cancel_url': reverse('download_list'),
    })


# Reports

@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'dashboard/report_list.html', {'reports': reports})

@login_required
def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report added successfully.')
            return redirect('report_list')
    else:
        form = ReportForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Report',
        'cancel_url': reverse('report_list'),
    })

@login_required
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully.')
            return redirect('report_list')
    else:
        form = ReportForm(instance=report)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Report',
        'cancel_url': reverse('report_list'),
    })

@login_required
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('report_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': report,
        'cancel_url': reverse('report_list'),
    })


# Notices

@login_required
def admin_notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'dashboard/notice_list.html', {'notices': notices})

@login_required
def admin_add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice added successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Notice',
        'cancel_url': reverse('notice_list'),
    })

@login_required
def admin_edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully.')
            return redirect('admin_notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Notice',
        'cancel_url': reverse('admin_notice_list'),
    })

@login_required
def admin_delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
        return redirect('admin_notice_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': notice,
        'cancel_url': reverse('admin_notice_list'),
    })


# career
@login_required
def admin_career_list(request):
    careers = Career.objects.all()
    return render(request, 'dashboard/career_list.html', {'careers': careers})

@login_required
def admin_add_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career added successfully.')
            return redirect('career_list')
    else:
        form = CareerForm()
    return render(request, 'dashboard/career_form.html', {
        'form': form,
        'title': 'Add Career',
        'cancel_url': reverse('admin_career_list'),
    })

@login_required
def admin_edit_career(request, pk):
    career = get_object_or_404(Career, pk=pk)
    if request.method == 'POST':
        form = CareerForm(request.POST, request.FILES, instance=career)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career updated successfully.')
            return redirect('admin_career_list')
    else:
        form = CareerForm(instance=career)
    return render(request, 'dashboard/career_form.html', {
        'form': form,
        'title': 'Edit Career',
        'cancel_url': reverse('admin_career_list'),
    })

@login_required
def admin_delete_career(request, pk):
    career = get_object_or_404(Career, pk=pk)
    if request.method == 'POST':
        career.delete()
        messages.success(request, 'Career deleted successfully.')
        return redirect('admin_career_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': career,
        'cancel_url': reverse('admin_career_list'),
    })


# CLIENT

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'dashboard/client_list.html', {'clients': clients})

@login_required
def admin_add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client added successfully.')
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Client',
        'cancel_url': reverse('client_list'),
    })

@login_required
def admin_edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client updated successfully.')
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Client',
        'cancel_url': reverse('client_list'),
    })

@login_required
def admin_delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        messages.success(request, 'Client deleted successfully.')
        return redirect('client_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': client,
        'cancel_url': reverse('client_list'),
    })


# NEWSLETTER SUBSCRIBERS

@login_required
def newsletter_list(request):
    subscribers = NewsletterSubscriber.objects.all()
    return render(request, 'dashboard/newsletter_list.html', {'subscribers': subscribers})

@login_required
def delete_newsletter_subscriber(request, pk):
    subscriber = get_object_or_404(NewsletterSubscriber, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        messages.success(request, 'Subscriber deleted.')
        return redirect('newsletter_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': subscriber,
        'cancel_url': reverse('newsletter_list'),
    })
@login_required
def export_newsletter_subscribers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="newsletter_subscribers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed At'])

    for sub in NewsletterSubscriber.objects.all():
        writer.writerow([sub.email, sub.subscribed_at.strftime('%Y-%m-%d %H:%M')])

    return response

@login_required
def organizationdetail_list(request):
    organizationdetails = OrganizationDetail.objects.all()
    return render(request, 'dashboard/organizationdetail_list.html', {'organizationdetails': organizationdetails})

@login_required
def add_organizationdetail(request):
    if OrganizationDetail.objects.exists():
        messages.warning(request, "Only one organization detail can be added. Please edit the existing one.")
        return redirect('organizationdetail_list')

    if request.method == 'POST':
        form = OrganizationDetailForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization details added successfully.')
            return redirect('organizationdetail_list')
    else:
        form = OrganizationDetailForm()

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Add Organization Details',
        'cancel_url': reverse('organizationdetail_list'),
    })

@login_required
def edit_organizationdetail(request, pk):
    obj = get_object_or_404(OrganizationDetail, pk=pk)

    if request.method == 'POST':
        form = OrganizationDetailForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization details updated successfully.')
            return redirect('organizationdetail_list')
    else:
        form = OrganizationDetailForm(instance=obj)

    return render(request, 'dashboard/generic_form.html', {
        'form': form,
        'title': 'Edit Organization Details',
        'cancel_url': reverse('organizationdetail_list'),
    })

@login_required
def delete_organizationdetail(request, pk):
    obj = get_object_or_404(OrganizationDetail, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Organization details deleted successfully.')
        return redirect('organizationdetail_list')
    return render(request, 'dashboard/confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse('organizationdetail_list'),
    })


# ---------- PHOTO VIEWS ----------

@login_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'dashboard/photo_list.html', {'photos': photos})
@login_required
def add_photo(request):
    form = PhotoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Photo added successfully.")
        return redirect('photo_list')
    return render(request, 'dashboard/photo_form.html', {
        'form': form,
        'title': 'Add Photo',
        'cancel_url': reverse('photo_list')
    })

@login_required
def edit_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    form = PhotoForm(request.POST or None, request.FILES or None, instance=photo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Photo updated successfully.")
        return redirect('photo_list')
    return render(request, 'dashboard/photo_form.html', {
        'form': form,
        'title': 'Edit Photo',
        'cancel_url': reverse('photo_list')
    })

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('photo_list')


# ---------- VIDEO VIEWS ----------

@login_required
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'dashboard/video_list.html', {'videos': videos})
@login_required
def add_video(request):
    form = VideoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Video added successfully.")
        return redirect('video_list')
    return render(request, 'dashboard/video_form.html', {
        'form': form,
        'title': 'Add Video',
        'cancel_url': reverse('video_list')
    })

@login_required
def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    form = VideoForm(request.POST or None, instance=video)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Video updated successfully.")
        return redirect('video_list')
    return render(request, 'dashboard/video_form.html', {
        'form': form,
        'title': 'Edit Video',
        'cancel_url': reverse('video_list')
    })
@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.delete()
    return redirect('video_list')




@login_required
def key_info_view(request):
    key_info, created = KeyInfo.objects.get_or_create(id=1)  # Always use the same row
    form = KeyInfoForm(request.POST or None, instance=key_info)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Key Strategy and Achievement updated successfully.")
        return redirect('key_info')

    return render(request, 'dashboard/key_info.html', {
        'form': form,
        'key_info': key_info
    })



def edit_organization_content(request):
    content, created = OrganizationContent.objects.get_or_create(id=1)  # Assuming only one instance
    if request.method == 'POST':
        form = OrganizationContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, "Content updated successfully.")
            return redirect('edit_organization_content')
    else:
        form = OrganizationContentForm(instance=content)
    return render(request, 'dashboard/edit_organization_content.html', {'form': form})


