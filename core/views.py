from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.admin_forms import TeamMemberForm
from .models import (
    Career, CareerApplication, ContactInfo, ContactMessage, CarouselItem, AboutImage, AboutInfo,
    Fact, Feature, Service, Project, TeamMember, Testimonial, FeatureImage,
    Report, Download, Notice, Client, NewsletterSubscriber, OrganizationContent,
    Photo, Video, KeyInfo,Governance
)
from .forms import PhotoForm, VideoForm, CareerApplicationForm
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
# Home Page View
def home(request):
    context = {
        'carousel_items': CarouselItem.objects.all(),
        'about_images': AboutImage.objects.all(),
        'about_info': AboutInfo.objects.first(),
        'facts': Fact.objects.all(),
        'feature_img': FeatureImage.objects.first(),
        'governance' : Governance.objects.all(),
        'features': Feature.objects.all(),
        'services': Service.objects.all(),
        'projects': Project.objects.all(),
        'team_members': TeamMember.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'contact_info': ContactInfo.objects.first(),
        'past_clients': Client.objects.filter(past_or_present='past'),
        'present_clients': Client.objects.filter(past_or_present='present'),
        'notices': Notice.objects.all().order_by('-published_at')[:3],
    }
    return render(request, 'home.html', context)


# Project Detail View
def project_detail(request, slug):
    # Get the project
    project = get_object_or_404(Project, slug=slug)
    
    # Get related projects with only the fields we need
    related_projects = Project.objects.filter(
        status=project.status
    ).exclude(
        id=project.id
    ).only(
        'id', 'title', 'short_description', 'slug', 'status', 'image'
    )[:5]
    
    return render(request, 'projects/detail.html', {
        'project': project,
        'related_projects': related_projects,
    })

def governance_view(request):
    governance = Governance.objects.all()
    about_images = AboutImage.objects.all(),
    return render(request, 'governance.html', {'governance': governance,'about_images':about_images})


# About Page View
def about(request):
    context = {
        'about_images': AboutImage.objects.all(),
        'about_info': AboutInfo.objects.first(),
        'organization_content': OrganizationContent.objects.first(),
        'teams': TeamMember.objects.all().order_by('name'),
        'key_info': KeyInfo.objects.all(),
        'governance': Governance.objects.all(),
    }
    return render(request, 'about.html', context)


# Static Pages
def services(request):
    context = {
        'services': Service.objects.all(),
        'testimonials': Testimonial.objects.all(),
    }

    return render(request, 'services.html', context)

from django.shortcuts import get_object_or_404

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related_services = Service.objects.exclude(id=service.id)[:5]
    return render(request, 'services/detail.html', {
        'service': service,
        'related_services': related_services})

def projects(request):
    # Only fetch the fields we need for the list view
    project_fields = ['id', 'title', 'short_description', 'slug', 'status', 'image']
    
    # Get projects without using prefetch_related on FileField
    ongoing_projects = Project.objects.filter(status='ongoing').only(*project_fields)
    completed_projects = Project.objects.filter(status='completed').only(*project_fields)

    context = {
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'projects.html', context)

def reports(request):
    reports = Report.objects.all().order_by('-created_at')  # latest first
    context = {'reports': reports}
    return render(request, 'reports.html', context)

def downloads(request):
    downloads = Download.objects.all().order_by('-uploaded_at')
    context = {'downloads': downloads}
    return render(request, 'downloads.html', context)

def notice(request):
    notices = Notice.objects.filter(is_active=True).order_by('-published_at')
    context = {
        'notices': notices,
        'title': 'News and Notices',
        'page_header': 'News and Notices',
        'breadcrumb_title': 'News and Notices'
    }
    return render(request, 'notice.html', context)


def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk, is_active=True)
    related_notices = Notice.objects.filter(is_active=True).exclude(pk=pk).order_by('-published_at')[:5]
    
    # Get the latest notices for the frontend view
    latest_notices = Notice.objects.filter(is_active=True).order_by('-published_at')[:10]
    
    context = {
        'notice': notice,  # For single notice view
        'notices': latest_notices,  # For list view fallback
        'related_notices': related_notices,
        'title': notice.title,
        'page_header': notice.title,
        'breadcrumb_title': 'Notice Details'
    }
    return render(request, 'notice.html', context)


# Contact Page View
def contact(request):
    contact_info = ContactInfo.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ContactMessage.objects.create(
                name=cd['name'],
                email=cd['email'],
                subject=cd['subject'],
                message=cd['message']
            )
            return render(request, 'contact.html', {
                'form': ContactForm(),
                'success': True,
                'contact_info': contact_info,
            })
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
        'contact_info': contact_info,
    })

def clients(request):
    clients = Client.objects.all()
    context = {'clients': clients}
    return render(request, 'clients.html', context)

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.info(request, "You're already subscribed.")
        else:
            messages.error(request, "Please enter a valid email.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def video(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'videogallery.html', { 'videos': videos})


def photo(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photogallery.html', {'photos': photos})



def key_info_view(request):
    # Get the KeyInfo instance (assuming you have one)
    key_info = KeyInfo.objects.first()
    
    context = {
        'key_info': key_info
    }
    return render(request, 'what_we_do.html', context)


def coverage(request):
    return render(request, 'coverage.html')


# Career Views
class CareerListView(ListView):
    model = Career
    template_name = 'career/list.html'
    context_object_name = 'careers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Career.objects.filter(
            closing_date__gte=timezone.now().date()
        ).order_by('-opening_date')
        return queryset


class CareerDetailView(DetailView):
    model = Career
    template_name = 'career/detail.html'
    context_object_name = 'career'
    
    def get_queryset(self):
        return Career.objects.filter(closing_date__gte=timezone.now().date())


class CareerCreateView(LoginRequiredMixin, CreateView):
    model = Career
    template_name = 'career/form.html'
    fields = ['title', 'description', 'opening_date', 'closing_date']
    success_url = reverse_lazy('career-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Career opportunity created successfully.')
        return super().form_valid(form)


class CareerUpdateView(LoginRequiredMixin, UpdateView):
    model = Career
    template_name = 'career/form.html'
    fields = ['title', 'description', 'opening_date', 'closing_date']
    
    def get_success_url(self):
        return reverse('career-detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Career opportunity updated successfully.')
        return super().form_valid(form)


@login_required
def career_delete(request, pk):
    career = get_object_or_404(Career, pk=pk)
    if request.method == 'POST':
        career.delete()
        messages.success(request, 'Career opportunity deleted successfully.')
        return redirect('career-list')
    return render(request, 'career/confirm_delete.html', {'career': career})


def career_apply(request, pk):
    career = get_object_or_404(Career, pk=pk)
    
    if request.method == 'POST':
        form = CareerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new CareerApplication instance
            CareerApplication.objects.create(
                career=career,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                resume=form.cleaned_data['resume'],
                message=form.cleaned_data.get('message', '')
            )
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('career_list')
    else:
        form = CareerApplicationForm()
    
    return render(request, 'career/apply.html', {
        'career': career,
        'form': form
    })

# Team Views
def team_list(request):
    team_members = TeamMember.objects.all()
    return render(request, 'team/list.html', {'team_members': team_members})

def team_detail(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    return render(request, 'team/detail.html', {'member': member})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member created successfully.')
            return redirect('team_list')
    else:
        form = TeamMemberForm()
    return render(request, 'team/form.html', {'form': form, 'action': 'Add'})

@login_required
def team_update(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully.')
            return redirect('team_list')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'team/form.html', {'form': form, 'action': 'Edit'})

@login_required
def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Team member deleted successfully.')
        return redirect('team_list')
    return render(request, 'team/confirm_delete.html', {'member': member})

# API Views
from rest_framework import generics, filters
from .serializers import TeamSerializer

class TeamListAPIView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'position']
    ordering_fields = ['name', 'position']

class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer


