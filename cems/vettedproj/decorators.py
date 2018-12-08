from django.core.exceptions import PermissionDenied

def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user, 'employee') and 
        		request.user.employee and 
        		request.user.employee.is_active and 
        		request.user.employee.company.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    return wrap


def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if hasattr(request.user.employee, 'is_admin') and
        		request.user.employee.is_admin and 
        		request.user.employee.company.is_active:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    return wrap