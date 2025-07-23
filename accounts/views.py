from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def login_redirect(request):
    """
    Redirects users to their appropriate dashboard after login based on their role.
    """
    if request.user.is_authenticated:
        if request.user.role == 'TEACHER':
            return redirect('teacher_dashboard')
        elif request.user.role == 'PARENT':
            return redirect('parent_dashboard')
    
    # As a fallback, if the user has no role or is not authenticated,
    # send them back to the login page.
    return redirect('login')