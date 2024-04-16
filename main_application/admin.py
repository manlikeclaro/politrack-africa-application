from django.contrib import admin

from main_application.models import Report, Blog, CustomerLead


# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'release_date')
    readonly_fields = ('created_on', 'slug',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug')


@admin.register(CustomerLead)
class CustomerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date')
