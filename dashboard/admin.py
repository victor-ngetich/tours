from django.contrib import admin
from .models import destination, package, booking, DestinationImage

class EventModelAdmin(admin.ModelAdmin):
    list_display = ["d_name", "d_location", "d_description", 'd_pic1', 'd_email']
    list_display_links = ["d_name"]
    list_filter = ["d_location"]
    list_per_page = 10
    list_editable = []
    search_fields = ["d_name","d_location"]

    class Meta:
        model = destination

class EventModelAdmin3(admin.ModelAdmin):
    list_display = ["destination", "image", "uploaded_at"]
    list_display_links = ["destination"]
    list_filter = ["destination"]
    list_per_page = 10
    list_editable = []
    search_fields = ["destination","image"]

    class Meta:
        model = DestinationImage

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["p_name", "p_category", "d_name","p_agency","p_price","p_duration",'p_description', 'p_reviews']
    list_display_links = ["p_name"]
    list_filter = ["p_category", "d_name"]
    list_per_page = 5
    list_editable = []
    search_fields = ["p_name", "p_category", "d_name"]

    class Meta:
        model = package

class EventModelAdmin2(admin.ModelAdmin):
    list_display = ["packages", "d_name", "user", 'date_added', 'p_price','t_number']
    list_display_links = ["packages"]
    list_filter = ["d_name", 'user']
    list_per_page = 10
    list_editable = []
    search_fields = ["packages","user"]

    class Meta:
        model = booking

admin.site.register(destination,EventModelAdmin)
admin.site.register(package,EventModelAdmin1)
admin.site.register(booking,EventModelAdmin2)
admin.site.register(DestinationImage,EventModelAdmin3)