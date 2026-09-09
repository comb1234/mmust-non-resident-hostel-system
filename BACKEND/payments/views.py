import uuid

from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from account.permissions import IsOwnerOrAdmin
from bookings.models import Booking

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(student=user)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'], url_path='stk-push')
    def stk_push(self, request):
        """Start a local STK simulation; completion happens through mock-complete."""
        booking_id = request.data.get('booking')
        if not booking_id:
            return Response({'detail': 'A booking is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = self.get_queryset().select_related('hostel', 'student').get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role != 'admin' and booking.student_id != request.user.id:
            return Response({'detail': 'You can only pay for your own booking.'}, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'cancelled':
            return Response({'detail': 'Cancelled bookings cannot be paid.'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.hostel.rooms_available < 1:
            return Response({'detail': 'This hostel has no rooms available.'}, status=status.HTTP_400_BAD_REQUEST)

        phone_number = booking.student.phone.strip()
        if not phone_number:
            return Response({'detail': 'Add a phone number to your profile before paying.'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.payments.filter(status='completed').exists():
            return Response({'detail': 'This booking has already been paid.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_payment = booking.payments.filter(status='pending').order_by('-created_at').first()
        if existing_payment:
            return Response({
                'message': f'Mock STK prompt is already pending for {phone_number}.',
                'payment': PaymentSerializer(existing_payment).data,
            }, status=status.HTTP_200_OK)

        checkout_request_id = f'MOCK-STK-{uuid.uuid4().hex[:16].upper()}'
        payment = Payment.objects.create(
            booking=booking,
            student=booking.student,
            amount=booking.hostel.price_per_semester,
            payment_method='M-Pesa STK (mock)',
            phone_number=phone_number,
            checkout_request_id=checkout_request_id,
            result_description='Mock STK prompt sent; awaiting customer approval',
            status='pending',
        )

        return Response({
            'message': f'Mock STK prompt sent to {phone_number}. Approve it to complete payment.',
            'payment': PaymentSerializer(payment).data,
            'booking_status': booking.status,
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='mock-complete')
    def mock_complete(self, request, pk=None):
        """Simulate the customer approving the STK prompt without contacting M-Pesa."""
        with transaction.atomic():
            payment = self.get_queryset().select_for_update().select_related('booking__hostel').get(pk=pk)
            if payment.status == 'completed':
                return Response({'message': 'Payment was already completed.', 'payment': PaymentSerializer(payment).data})
            if payment.status == 'failed':
                return Response({'detail': 'This payment attempt has failed.'}, status=status.HTTP_400_BAD_REQUEST)
            booking = payment.booking
            hostel = booking.hostel
            if booking.status == 'cancelled':
                payment.status = 'failed'
                payment.result_description = 'Booking was cancelled before STK approval'
                payment.save(update_fields=['status', 'result_description', 'updated_at'])
                return Response({'detail': 'Cancelled bookings cannot be paid.'}, status=status.HTTP_400_BAD_REQUEST)
            if hostel.rooms_available < 1:
                payment.status = 'failed'
                payment.result_description = 'No rooms were available when payment was approved'
                payment.save(update_fields=['status', 'result_description', 'updated_at'])
                return Response({'detail': 'No rooms are available.'}, status=status.HTTP_400_BAD_REQUEST)

            payment.status = 'completed'
            payment.transaction_id = f'MOCK-MPESA-{uuid.uuid4().hex[:10].upper()}'
            payment.result_description = 'Mock STK approval received successfully'
            payment.save(update_fields=['status', 'transaction_id', 'result_description', 'updated_at'])
            booking.status = 'confirmed'
            booking.save(update_fields=['status', 'updated_at'])
            hostel.rooms_available -= 1
            hostel.save(update_fields=['rooms_available', 'updated_at'])

        return Response({
            'message': f'Mock payment completed for {payment.phone_number}.',
            'payment': PaymentSerializer(payment).data,
            'booking_status': booking.status,
        })