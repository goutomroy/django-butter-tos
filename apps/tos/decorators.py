from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework.reverse import reverse
from .models import TermsOfService


def terms_checker(view_func):

    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):

        terms = TermsOfService.get_pending_terms(args[1].user)
        if not terms.exists():
            return view_func(*args, **kwargs)

        return HttpResponseRedirect(reverse('tos:terms_of_service-pending-terms', request=args[1]))
    return _wrapped_view
