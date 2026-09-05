from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Count, Sum
from account.models import User
from hostels.models import Hostel
from bookings.models import Booking
from payments.models import Payment
from complaints.models import Complaint
from maintenance.models import MaintenanceRequest

class DashboardStatsView(APIView):
    """Return aggregated statistics for admin dashboard."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = {
            'total_students': User.objects.filter(role='student').count(),
            'total_hostels': Hostel.objects.count(),
            'total_bookings': Booking.objects.count(),
            'total_payments': Payment.objects.count(),
            'total_complaints': Complaint.objects.count(),
            'total_maintenance': MaintenanceRequest.objects.count(),
            'revenue': Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0,
            'bookings_by_status': list(Booking.objects.values('status').annotate(count=Count('id'))),
            'payments_by_status': list(Payment.objects.values('status').annotate(count=Count('id'))),
            'hostels_occupancy': list(Hostel.objects.values('name', 'rooms_available', 'total_rooms')),
        }
        return Response(stats)