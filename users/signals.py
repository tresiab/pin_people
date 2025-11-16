from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Log that user logged in.
    Distinguish between admin login and site login.
    """
    # Using resolver_match is more reliable than "request.path.startswith"
    # request.path.startswith can produce false positives if another
    # route starts with "/admin/"
    if not getattr(request, "resolver_match", None):
        return  # Skip logging when there is no resolver_match (this is the case when running tests)

    if request.resolver_match.view_name == "admin:login":
        change_message = "User logged in via admin site."
    else:
        change_message = "User logged in via site."

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=None,
        object_id=None,
        object_repr=str(user),
        action_flag=CHANGE,
        change_message=change_message,
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    Log that user logged out.
    Distinguish between admin login and site login.
    """
    if not user:
        return

    # Using resolver_match is more reliable than "request.path.startswith"
    # request.path.startswith can produce false positives if another
    # route starts with "/admin/"
    if not getattr(request, "resolver_match", None):
        return  # Skip logging when there is no resolver_match (this is the case when running tests)

    if request.resolver_match.view_name == "admin:logout":
        change_message = "User logged out via admin site."
    else:
        change_message = "User logged out via site."

    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=None,
        object_id=None,
        object_repr=str(user),
        action_flag=CHANGE,
        change_message=change_message,
    )
