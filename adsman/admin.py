from tourprom.adsman.models import *
from django.contrib import admin

admin.site.register(AdsControl)
class AdsPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'visible')
admin.site.register(AdsPage, AdsPageAdmin)
admin.site.register(AdsPlacedControl)
admin.site.register(AdsPost)
admin.site.register(AdsPostEntry)
