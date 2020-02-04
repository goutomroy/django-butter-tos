from apps.tos.decorators import redirect_to_terms
from apps.tos.utils import is_eligible_to_redirect


class TermsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if is_eligible_to_redirect(request):
            return redirect_to_terms(request)

        response = self.get_response(request)
        return response


