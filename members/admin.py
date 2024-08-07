from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


# Register your models here.

class UserAdminConfig(UserAdmin):
    model = Member
    search_fields = ('email', 'username', 'first_name')
    list_filter = ('email', 'username', 'first_name', 'is_staff', 'is_active')
    ordering = ('-start_date',)
    list_display = (
        'email',
        'id',
        'username',
        'first_name',
        'contact',
        'address',
        'is_staff',
        'is_superuser',
        'is_active',
    )
    fieldsets = (
                    (None, {'fields': ('email', 'id', 'username', 'first_name',)}),
                    ('permissions', {'fields': ('is_staff', 'is_active',)}),
                     ('personal', {'fields': ('about', 'contact', 'address',)})
                     )
    formfield_overrides = {
        Member.about: {'widget': Textarea(attrs={'rows': 20, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'contact', 'address','password1', 'password2', 'is_active', 'is_staff'),
        }),
    )


admin.site.register(Member, UserAdminConfig)
