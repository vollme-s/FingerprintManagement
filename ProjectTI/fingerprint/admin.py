from django.contrib import admin
from fingerprint.models import Fingerprint, Door, Log, Privilege


class LogAdmin(admin.ModelAdmin):
    list_display = ['door', 'user', 'datetime']
    list_filter = ['datetime', 'door', 'user']
    search_fields = ['user__user__username', 'message', 'door__name']

# Register your models here.
admin.site.register(Fingerprint)
admin.site.register(Door)
admin.site.register(Log, LogAdmin)
admin.site.register(Privilege)


