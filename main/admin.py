from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin

from main.resources import *


@admin.register(LogEntry)
class LogEntryAdmin(ImportExportModelAdmin):
    date_hierarchy = "action_time"

    list_filter = ["user", "content_type", "action_flag"]

    search_fields = ["object_repr", "change_message"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse(
                    "admin:%s_%s_change" % (ct.app_label, ct.model),
                    args=[obj.object_id],
                ),
                escape(obj.object_repr),
            )
        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


class UserResourceAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    search_fields = ["email"]
    list_display = ('id',
                    'email',
                    'is_superuser',
                    'is_active',
                    "phone_number",
                    "first_name",
                    "last_name",
                    "country",
                    "referral_code",
                    "created_at",
                    "updated_at",
                    )
    
class TicketTypeResourceAdmin(ImportExportModelAdmin):
    resource_class = TicketTypeResource
    search_fields = ["ticket_name"]
    list_filter = ["is_active"]
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
class GameTicketResourceAdmin(ImportExportModelAdmin):
    resource_class = GameTicketResource
    search_fields = ["email"]
    list_filter = ["is_paid"]
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
class GameBatchResourceAdmin(ImportExportModelAdmin):
    resource_class = GameBatchResource
    search_fields = ["batch_id"]
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
class WinnerTableResourceAdmin(ImportExportModelAdmin):
    resource_class = WinnerTableResource
    search_fields = ["email"]
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]
    
    
admin.site.register(User, UserResourceAdmin)
admin.site.register(TicketType, TicketTypeResourceAdmin)
admin.site.register(GameTicket, GameTicketResourceAdmin)
admin.site.register(GameBatch, GameBatchResourceAdmin)
admin.site.register(WinnerTable, WinnerTableResourceAdmin)