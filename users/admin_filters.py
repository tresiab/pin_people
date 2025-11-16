from django.contrib.admin import SimpleListFilter


class AdminLoginLogoutFilter(SimpleListFilter):
    """
    Custom admin list filter for distinguishing between user login and logout events.
    """

    title = "Login/Logout"
    parameter_name = "login_logout"

    def lookups(self, request, model_admin):
        return (
            ("login", "Login"),
            ("logout", "Logout"),
        )

    def queryset(self, request, queryset):
        if self.value() == "login":
            return queryset.filter(change_message__icontains="logged in")
        if self.value() == "logout":
            return queryset.filter(change_message__icontains="logged out")
        return queryset
