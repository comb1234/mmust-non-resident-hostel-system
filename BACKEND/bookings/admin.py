from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('student', 'hostel', 'status', 'semester', 'created_at')
	list_editable = ('status',)
	search_fields = ('student__username', 'hostel__name')
	list_filter = ('status', 'semester')
