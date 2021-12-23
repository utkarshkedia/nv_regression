from django.http import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                groups = []
                Access = False
                if request.user.groups.exists():
                    for group in request.user.groups.all():
                        groups.append(group.name)
                for group in groups:
                    if group in allowed_roles:
                        Access = True
                if Access:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse("You don't have the permission to complete this action")
            else:
                return redirect("/")
        return wrapper_func
    return decorator