from django.core.cache import cache
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from apps.tos.models import TermsOfService, UserTermsOfService
from apps.tos.serializers import TermsOfServiceSerializer, UserTermsOfServiceSerializer


class UserTermsOfServiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserTermsOfServiceSerializer
    queryset = UserTermsOfService.objects.all()


class TermsOfServiceViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TermsOfServiceSerializer

    def get_queryset(self):
        return TermsOfService.get_pending_terms(self.request.user)

    def get_template_names(self):
        app = self.request.resolver_match.app_name
        templates = {
            'list': [f"{app}/list.html", "list.html"],
            'retrieve': [f"{app}/retrieve.html", "retrieve.html"]
        }

        if self.action in templates.keys():
            selected_templates = templates[self.action]
        else:
            selected_templates = ['rest_framework/api.html']
        return selected_templates

    @action(detail=False, methods=['post'])
    def accept_terms(self, request):
        tos_ids = [request.data[k] for k in request.data if k.startswith('tos-')]
        for tos_id in tos_ids:
            tos = TermsOfService.objects.get(id=int(tos_id))
            UserTermsOfService.objects.get_or_create(user=request.user, terms=tos)

        cache.delete(f"pending_terms_{request.user.id}")

        if request.accepted_renderer.format == 'html':
            if 'next' in request.data:
                return HttpResponseRedirect(request.data['next'])
            else:
                return HttpResponseRedirect(reverse('tos:terms_of_service-list', request=request))
        else:
            return Response(data={'detail': 'All pending terms accepted.'}, status=status.HTTP_202_ACCEPTED)

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            print(f"-----{type(self.get_queryset())}")
            data = {'tos_list': self.get_queryset()}
            print(f"-----{type(data['tos_list'])}")
            return Response(data)
        return super().list(request, *args, **kwargs)




