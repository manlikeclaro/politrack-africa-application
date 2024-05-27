from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from main_application.models import Report, Blog, CustomerMessage

# Unregister the default Models
admin.site.unregister(User)
admin.site.unregister(Group)


# Register your models here.
@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_users')

    def num_users(self, obj):
        return obj.user_set.count()

    num_users.short_description = 'Number of Users'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_groups',)

    def get_groups(self, obj):
        if not obj.groups.exists():
            return '- '
        return ', '.join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'

    # def get_queryset(self, request):
    #     query = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return query
    #     return query.filter(id=request.user.id)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:  # Superuser can change all fields
            return super().get_fieldsets(request, obj=obj)
        else:
            return (
                ('Account info', {'fields': ('username', 'first_name', 'last_name', 'email')}),
            )

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or obj == request.user:
            return True
        return False


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_name', 'release_date', 'author')
    readonly_fields = ('created_on', 'slug', 'author')
    ordering = ('-release_date',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If it's a new object
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser or obj.author == request.user:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser or obj.author == request.user:
                return True
        return False


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fields = ('title', 'image', 'content', 'author', 'slug', 'created_at', 'updated_at')
    list_display = ('title', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'slug', 'author')
    ordering = ('-created_at',)
    filter = ('author',)

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
        if obj is not None:
            if request.user.is_superuser or obj.author == request.user:
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser or obj.author == request.user:
                return True
        return False


@admin.register(CustomerMessage)
class CustomerMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'date', 'status')
    readonly_fields = ('name', 'email', 'subject', 'message', 'date')

    def has_change_permission(self, request, obj=None):
        if request.user:
            return True  # Users can update message status
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True  # Superuser can delete any message
        return False
