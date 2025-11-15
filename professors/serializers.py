from rest_framework import serializers
from .models import Professor


class ProfessorSerializer(serializers.ModelSerializer):
    title_display = serializers.CharField(source='get_title_display', read_only=True)
    
    class Meta:
        model = Professor
        fields = [
            'id', 'name', 'title', 'title_display', 'department', 'email',
            'office', 'phone', 'research_interests', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
