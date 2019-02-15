from django.contrib import admin
from .models import destination, package
 
class EventModelAdmin(admin.ModelAdmin):
    list_display = ["d_name", "d_location", "d_description", 'd_pics','d_payment_info','d_days', 'd_email']
    list_display_links = ["d_name"]
    list_filter = ["d_location"]
    list_per_page = 10
    list_editable = []
    search_fields = ["d_name","d_location"]

    class Meta:
        model = destination

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["p_name", "p_category", "d_name","p_agent","p_price","p_duration",'p_description', 'p_reviews']
    list_display_links = ["p_name"]
    list_filter = ["p_category", "d_name"]
    list_per_page = 5
    list_editable = []
    search_fields = ["p_name", "p_category", "d_name"]

    class Meta:
        model = package

admin.site.register(destination,EventModelAdmin)
admin.site.register(package,EventModelAdmin1)