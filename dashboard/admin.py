from django.contrib import admin
from .models import destination, package
 
class EventModelAdmin(admin.ModelAdmin):
    list_display = ["d_name", "d_location", "d_category", "d_description", 'd_pics','d_payment_info','d_days', 'd_reviews', 'd_email']
    list_display_links = ["d_name"]
    list_filter = ["d_location","d_category"]
    list_per_page = 10
    list_editable = []
    search_fields = ["d_name","d_location", "d_category"]

    class Meta:
        model = destination

class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["p_name", "d_name","p_guide","p_package_price","p_package_size","p_duration",'p_description']
    list_display_links = ["p_name"]
    list_filter = ["d_name","p_package_size"]
    list_per_page = 5
    list_editable = []
    search_fields = ["p_name","d_name"]

    class Meta:
        model = package

admin.site.register(destination,EventModelAdmin)
admin.site.register(package,EventModelAdmin1)