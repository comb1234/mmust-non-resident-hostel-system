from rest_framework import viewsets, permissions
from .models import MaintenanceRequest
from .serializers import MaintenanceRequestSerializer
from account.permissions import IsOwnerOrAdmin

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return MaintenanceRequest.objects.all()
        return MaintenanceRequest.objects.filter(student=user)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]