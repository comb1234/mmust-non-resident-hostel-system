# Register models for admin
from django.contrib import admin
from .models import Hostel


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
	list_display = ('name', 'location', 'gender', 'price_per_semester', 'rooms_available', 'total_rooms', 'rating')
	list_editable = ('price_per_semester',)
	search_fields = ('name', 'location')
	list_filter = ('gender',)
	readonly_fields = ('created_at', 'updated_at')
	fieldsets = (
		(None, {
			'fields': ('name', 'description', 'location', 'distance')
		}),
		('Availability & Pricing', {
			'fields': ('price_per_semester', 'rooms_available', 'total_rooms')
		}),
		('Extras', {
			'fields': ('gender', 'amenities', 'images', 'rating', 'contact')
		}),
		('Timestamps', {
			'fields': ('created_at', 'updated_at')
		}),
	)

