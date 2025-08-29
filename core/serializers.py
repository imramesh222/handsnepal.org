from rest_framework import serializers
from .models import Notice, TeamMember, Career

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'image', 'attachment', 'published_at']
        read_only_fields = ['published_at']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'position', 'photo', 'facebook', 'phone', 'email','description']
        read_only_fields = ['id']


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'title', 'description', 'opening_date', 'closing_date']
        read_only_fields = ['id']

