from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    prerequisite_codes = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'code', 'credit', 'description', 'course_level',
            'prerequisites', 'prerequisite_codes', 'is_elective', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_prerequisite_codes(self, obj):
        return [prereq.code for prereq in obj.prerequisites.all()]
