from django.contrib import admin
from .models import *



class EventItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)

admin.site.register(Pack)
admin.site.register(Subscription)
admin.site.register(Item)
admin.site.register(EventItem, EventItemAdmin)
admin.site.register(EventSubscription)
admin.site.register(SponsorEvent)
