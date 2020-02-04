import logging
from functools import wraps
from .utils import redirect_to_terms, is_eligible_to_redirect

logger = logging.getLogger(__name__)


def terms_checker(view_func):

    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):

        if is_eligible_to_redirect(request):
            return redirect_to_terms(request)

        return view_func(view, request, *args, **kwargs)

    return _wrapped_view



