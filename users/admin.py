from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from backend.models import Topics
from .froms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = User

    list_display = ('username', 'is_staff', 'is_active', 'topics')
    list_filter = ('username', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    @admin.display(description="Topics which user has created")
    def topics(self, obj):
        topics_names = [f'<li><a href="/admin/backend/topics/{x.id}/change/">{x.topic_name}</a></li>' for x in
                        Topics.objects.filter(owner=obj)]
        return format_html(f'<ul>{" ".join(topics_names)}</ul>')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
