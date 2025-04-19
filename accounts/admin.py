from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, UserProfile


class UserModelAdmin(UserAdmin):
    model = User
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
    ]

    list_filter = ["is_staff", "is_superuser", "is_active"]

    # Show information in admin panel category-wised
    fieldsets = [
        ("User Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                # Its a css class to make a full width admin layout
                "classes": ["wide"],
                # This fields will appear in admin panel add user form
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email"]
    ordering = ["email", "id"]
    filter_horizontal = ["groups", "user_permissions"]


# Now register the new UserModelAdmin
admin.site.register(User, UserModelAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'state', 'country', 'address']

