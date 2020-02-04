from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework.permissions import SAFE_METHODS
from rest_framework.reverse import reverse

TERMS_PROTECTED_PATH = set(getattr(settings, "TERMS_PROTECTED_PATH", []) + ['/admin/', '/tos/'])
DEFAULT_TERMS_SLUG = getattr(settings, "DEFAULT_TERMS_SLUG", "butter-tos")
TERMS_CACHE_SECONDS = int(getattr(settings, "TERMS_CACHE_SECONDS", 60))


def is_eligible_to_redirect(request):
    from apps.tos.models import TermsOfService
    return request.user.is_authenticated and not is_path_protected(request.path_info) and \
           request.method in SAFE_METHODS and TermsOfService.get_pending_terms(request.user).exists()


def redirect_to_terms(request):
    reverse_url = reverse('tos:terms_of_service-list', request=request)
    reverse_url += f"?next={request.get_full_path()}"
    return HttpResponseRedirect(reverse_url)


def is_path_protected(current_path):
    for path in TERMS_PROTECTED_PATH:
        if current_path.startswith(path):
            return True
    return False
