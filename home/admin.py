from django.contrib import admin
from .models import information,User,job
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):

     fieldsets = (
        ("AUTHENTICATION", {
            'fields': ('username', 'password','security')
        }),


        ('CONTACT INFORMATION', {
            'fields': ('name', 'email', 'phone','whatsapp')
        }),


        ('ACCOUNT INFORMATION', {
                    'fields': ( 'date_joined','delivery','last_login')
                }),

        ('PERMISSIONS', {
            'fields': (
                 'is_staff', 'is_superuser','is_active',
                'groups', 'user_permissions'
                )
        })

    )

admin.site.register(information)
admin.site.register(job)
admin.site.register(User, CustomUserAdmin)