from datetime import date
from rest_framework import generics, permissions, filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.utils import timezone
from .models import Notice, TeamMember, Career
from .serializers import NoticeSerializer, TeamSerializer, CareerSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class NoticeListAPIView(generics.ListAPIView):
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        # Get only active notices, ordered by publish date (newest first)
        # and limit to 5 most recent notices
        return Notice.objects.filter(
            is_active=True
        ).order_by('-published_at')[:5]

class NoticeDetailAPIView(generics.RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.AllowAny]

class TeamListAPIView(generics.ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'position']
    ordering_fields = ['name', 'position']
    ordering = ['name']

class TeamDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Only allow updating if the user is authenticated
        if self.request.user.is_authenticated:
            serializer.save()

    def perform_destroy(self, instance):
        # Only allow deletion if the user is authenticated
        if self.request.user.is_authenticated:
            instance.delete()


class CareerListAPIView(generics.ListCreateAPIView):
    """
    API endpoint that lists all active career opportunities or creates a new one.
    """
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['opening_date', 'closing_date']
    ordering = ['-opening_date']

    def get_queryset(self):
        # Only show active career opportunities (not expired)
        today = timezone.now().date()
        return Career.objects.filter(
            closing_date__gte=today
        ).order_by('-opening_date')

    def perform_create(self, serializer):
        # Only allow creation if the user is authenticated
        if self.request.user.is_authenticated:
            serializer.save()


class CareerDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that retrieves, updates, or deletes a specific career opportunity.
    """
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Only allow updating if the user is authenticated
        if self.request.user.is_authenticated:
            serializer.save()

    def perform_destroy(self, instance):
        # Only allow deletion if the user is authenticated
        if self.request.user.is_authenticated:
            instance.delete()


