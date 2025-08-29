from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Notice, Career, CareerApplication
from .forms import NoticeForm, CareerForm

@login_required
def admin_notice_list(request):
    notices = Notice.objects.all().order_by('-published_at')
    return render(request, 'dashboard/notice_list.html', {'notices': notices})

@login_required
def admin_add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.save()
            messages.success(request, 'Notice added successfully!')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    
    return render(request, 'dashboard/notice_form.html', {
        'title': 'Add New Notice',
        'form': form
    })

@login_required
def admin_edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notice updated successfully!')
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    
    return render(request, 'dashboard/notice_form.html', {
        'title': 'Edit Notice',
        'form': form
    })

@login_required
def admin_delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, 'Notice deleted successfully!')
        return redirect('notice_list')
    
    return render(request, 'dashboard/confirm_delete.html', {
        'title': 'Delete Notice',
        'object': notice,
        'cancel_url': 'notice_list'
    })

# Career Management Views
@login_required
def admin_career_list(request):
    careers = Career.objects.all().order_by('-opening_date')
    return render(request, 'dashboard/career_list.html', {'careers': careers})

@login_required
def admin_add_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST)
        if form.is_valid():
            career = form.save(commit=False)
            career.save()
            messages.success(request, 'Career opportunity added successfully!')
            return redirect('admin_career_list')
    else:
        form = CareerForm()
    
    return render(request, 'dashboard/career_form.html', {
        'title': 'Add New Career Opportunity',
        'form': form,
        'cancel_url': 'admin_career_list'
    })

@login_required
def admin_edit_career(request, pk):
    career = get_object_or_404(Career, pk=pk)
    
    if request.method == 'POST':
        form = CareerForm(request.POST, instance=career)
        if form.is_valid():
            form.save()
            messages.success(request, 'Career opportunity updated successfully!')
            return redirect('admin_career_list')
    else:
        form = CareerForm(instance=career)
    
    return render(request, 'dashboard/career_form.html', {
        'title': 'Edit Career Opportunity',
        'form': form,
        'cancel_url': 'admin_career_list'
    })

@login_required
def admin_delete_career(request, pk):
    career = get_object_or_404(Career, pk=pk)
    if request.method == 'POST':
        career.delete()
        messages.success(request, 'Career opportunity deleted successfully!')
        return redirect('admin_career_list')
    
    return render(request, 'dashboard/confirm_delete.html', {
        'title': 'Delete Career Opportunity',
        'object': career,
        'cancel_url': 'admin_career_list'
    })

@login_required
def admin_career_application_list(request):
    applications = CareerApplication.objects.select_related('career').order_by('-applied_at')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        applications = applications.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(career__title__icontains=search_query)
        )
    
    # Filter by view status
    view_status = request.GET.get('view_status', '')
    if view_status == 'viewed':
        applications = applications.filter(is_viewed=True)
    elif view_status == 'unviewed':
        applications = applications.filter(is_viewed=False)
    
    # Pagination
    paginator = Paginator(applications, 20)  # Show 20 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Career Applications',
        'applications': page_obj,
        'search_query': search_query,
        'view_status': view_status,
        'total_applications': applications.count(),
    }
    
    return render(request, 'dashboard/career/application_list.html', context)


@login_required
def mark_application_viewed(request, pk):
    if request.method == 'POST':
        from django.http import JsonResponse
        try:
            application = CareerApplication.objects.get(pk=pk)
            if not application.is_viewed:
                application.is_viewed = True
                application.save()
            return JsonResponse({'success': True})
        except CareerApplication.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Application not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
