from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import destination, package, booking, Hotel, payment

class EventModelAdmin(admin.ModelAdmin):
    list_display = ["d_name", "d_location", "short_description", 'd_pic1', 'd_pic2', 'd_pic3', 'd_email', 'd_reviews', 'd_uploaded_at']
    list_display_links = ["d_name", 'd_pic1', 'd_pic2', 'd_pic3']
    list_filter = ["d_location", "d_name"]
    # list_per_page = 10
    list_editable = []
    search_fields = ["d_name","d_location", "d_phone", "d_email"]

    class Meta:
        model = destination

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["p_name", "p_category", "d_name", 'p_agency', 'agency', 'agency_phone', 'pricep_adult', 'pricep_kid', 'from_day', 'to_day', 'p_slots', 'available', "short_description",]
    list_display_links = ["p_name"]
    list_filter = ["d_name", "p_category", "p_agency", "from_day", "available"]
    list_per_page = 10
    list_editable = []
    search_fields = ["p_name", "d_name", "p_category", "p_agency", "available"]

    class Meta:
        model = package

class EventModelAdmin2(admin.ModelAdmin):
    list_display = ["p_name2", "d_name", 'agency', "user", "hotel", "adults", "kids", 'pricep_adult', 'pricep_kid', 'days', 'start_date', 'end_date', "date_added"]
    list_display_links = ["p_name2"]
    list_filter = ['user', "d_name", "agency", "hotel", "start_date"]
    list_per_page = 10
    list_editable = []
    search_fields = ["p_name2", "d_name", "user"]

    class Meta:
        model = booking

class EventModelAdmin3(admin.ModelAdmin):
    list_display = ["h_name", "destination", "pricep_adult", 'pricep_kid']
    list_display_links = ["h_name"]
    list_filter = ["destination"]
    list_per_page = 10
    list_editable = []
    search_fields = ["h_name","destination"]

    class Meta:
        model = Hotel

class EventModelAdmin4(admin.ModelAdmin):
    list_display = ["booking", "agency", "user", "amountpaid", "transaction_status", "transaction_id", "hotel", "adults", "kids", 'pricep_adult', 'pricep_kid', 'days', 'start_date', 'end_date', "date_added", "date_paid"]
    list_display_links = ["booking"]
    list_filter = ['user', "booking", "agency", "hotel", "transaction_status", "start_date"]
    list_per_page = 10
    list_editable = []
    search_fields = ["user", "booking", "transaction_id", "agency"]

    class Meta:
        model = payment

class EventModelAdmin5(UserAdmin):
    list_display = ['username','email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_per_page = 10
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    actions = ['make_active', ]

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Make User Active"

    class Meta:
        model = User


admin.site.site_header = 'The Kenyan Thrill Administration'
admin.site.register(destination,EventModelAdmin)
admin.site.register(package,EventModelAdmin1)
admin.site.register(booking,EventModelAdmin2)
admin.site.register(Hotel,EventModelAdmin3)
admin.site.register(payment,EventModelAdmin4)
admin.site.unregister(User)
admin.site.register(User,EventModelAdmin5)