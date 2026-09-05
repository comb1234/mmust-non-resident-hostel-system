from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'student', 'student_name', 'subject', 'description',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['student', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)