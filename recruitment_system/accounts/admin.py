from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HirerProfile, CandidateProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(HirerProfile)
admin.site.register(CandidateProfile)