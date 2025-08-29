from .models import OrganizationDetail

def organization_details(request):
    details = OrganizationDetail.objects.first()
    return {'org_details': details}
