from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    booking_details = serializers.CharField(source='booking.__str__', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'booking', 'booking_details', 'student', 'student_name',
                  'amount', 'payment_method', 'transaction_id', 'status', 'created_at', 'updated_at']
        read_only_fields = ['student', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)