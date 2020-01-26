from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework.permissions import SAFE_METHODS
from rest_framework.reverse import reverse
from .models import TermsOfService


def terms_checker(view_func):

    @wraps(view_func)
    def _wrapped_view(view, request, *args, **kwargs):

        if request.method in SAFE_METHODS and TermsOfService.get_pending_terms(request.user).exists():
            reverse_url = reverse('tos:terms_of_service-list', request=request)
            if request.accepted_renderer.format == 'html':
                reverse_url += f"?next={request.get_full_path()}"
            return HttpResponseRedirect(reverse_url)

        return view_func(view, request, *args, **kwargs)

    return _wrapped_view


