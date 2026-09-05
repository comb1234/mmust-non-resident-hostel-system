from rest_framework import viewsets, permissions, filters
from .models import Hostel
from .serializers import HostelSerializer
from account.permissions import IsAdminUser

class HostelViewSet(viewsets.ModelViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location', 'gender']
    ordering_fields = ['price_per_semester', 'rating', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [permissions.AllowAny()]