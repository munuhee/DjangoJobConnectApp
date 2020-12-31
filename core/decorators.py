from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

def userplan_required(plan_types=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.userplan.plan_type in plan_types:
                return viwe_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('plan'))
            return wrap
        return decorator
    