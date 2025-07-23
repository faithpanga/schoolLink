from django.http import HttpResponseForbidden


def role_required(role):
    """
    A decorator that checks if a user is authenticated and has a specific role.
    """

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Check 1: Is the user logged in?
            if not request.user.is_authenticated:
                # This will usually be caught by @login_required, but it's good practice.
                return HttpResponseForbidden("Authentication required.")

            # Check 2: Does the user have the required role?
            if request.user.role != role:
                return HttpResponseForbidden(
                    "You do not have permission to view this page."
                )

            # If both checks pass, proceed to the original view function.
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
