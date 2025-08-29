from .models import OrganizationDetail, Notice

def organization_details(request):
    details = OrganizationDetail.objects.first()
    return {'org_details': details}

def notice_processor(request):
    active_notices = Notice.objects.filter(is_active=True).order_by('-published_at')
    return {'notices': active_notices}
