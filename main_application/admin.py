from django.contrib import admin

from main_application.models import Report, Blog, CustomerMessage


# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'release_date', 'author')
    readonly_fields = ('created_on', 'slug', 'author')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser can update all reports
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser can delete any report
        if obj is not None and obj.author != request.user:
            return False
        return True


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'image', 'content', 'author', 'slug', 'created_at', 'updated_at')
    filter = ('author',)
    list_display = ('title', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug', 'author')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     query = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return query  # Superuser can see all blogs
    #     return query.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.author != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser can delete any blog
        if obj is not None and obj.author != request.user:
            return False
        return True


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date')
