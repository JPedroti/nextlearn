from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def papel_requerido(papel):
    """Libera a view só para usuários logados com o papel indicado (senão, erro 403)."""

    def decorator(view):
        @wraps(view)
        @login_required
        def _view(request, *args, **kwargs):
            if request.user.papel != papel:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return _view

    return decorator
