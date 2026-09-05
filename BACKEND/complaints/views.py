from rest_framework import viewsets, permissions
from .models import Complaint
from .serializers import ComplaintSerializer
from account.permissions import IsOwnerOrAdmin

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Complaint.objects.all()
        return Complaint.objects.filter(student=user)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]