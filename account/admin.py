from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from account.models import User

class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ('email','name')
    fieldsets = (
        (None,{'fields':('email','password')}),
        (_('Personal Info'),{'fields':('name','verify')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email', 'password1', 'password2','is_active','is_staff','is_superuser'),
        }),
    )

admin.site.register(User,UserAdmin)