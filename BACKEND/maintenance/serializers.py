from rest_framework import serializers
from .models import MaintenanceRequest

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'student', 'student_name', 'hostel', 'hostel_name',
                  'issue_type', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['student', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)