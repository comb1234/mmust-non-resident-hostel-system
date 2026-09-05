from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api/auth/', include('account.urls')),
    path('api/hostels/', include('hostels.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/complaints/', include('complaints.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/announcements/', include('announcements.urls')),
    path('api/reports/', include('reports.urls')),
]