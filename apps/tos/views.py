import logging

from django.core.cache import cache
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from apps.tos.models import TermsOfService, UserTermsOfService
from apps.tos.serializers import TermsOfServiceSerializer, UserTermsOfServiceSerializer

LOGGER = logging.getLogger(name="terms_of_services")


class UserTermsOfServiceViewSet(viewsets.ModelViewSet):
    serializer_class = UserTermsOfServiceSerializer
    queryset = UserTermsOfService.objects.all()


class TermsOfServiceViewSet(viewsets.ModelViewSet):
    serializer_class = TermsOfServiceSerializer
    queryset = TermsOfService.objects.all()

    def get_template_names(self):
        app = self.request.resolver_match.app_name
        templates = {
            'list': [f"{app}/list.html", "list.html"],
            'pending_terms': [f"{app}/pending_terms.html", "pending_terms.html"],
            'retrieve': [f"{app}/retrieve.html", "retrieve.html"],
            'create': [f"{app}/create.html", "create.html"],
            'update': [f"{app}/update.html", "update.html"],
            'partial_update': [f"{app}/partial_update.html", "partial_update.html"],
            'delete': [f"{app}/destroy.html", "destroy.html"],
        }

        if self.action in templates.keys():
            selected_templates = templates[self.action]
        else:
            selected_templates = ['rest_framework/api.html']
        return selected_templates

    @action(detail=False)
    def pending_terms(self, request):
        terms = TermsOfService.get_pending_terms(request.user)
        if request.accepted_renderer.format == 'html':
            data = {'tos_list': terms}
            return Response(data)
        else:
            serializer = TermsOfServiceSerializer(terms, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def accept_terms(self, request):
        tos_ids = [request.data[k] for k in request.data if k.startswith('tos-')]
        for tos_id in tos_ids:
            tos = TermsOfService.objects.get(id=int(tos_id))
            UserTermsOfService.objects.get_or_create(user=request.user, terms=tos)

        cache.delete(f"pending_terms_{request.user.id}")

        if request.accepted_renderer.format == 'html':
            return HttpResponseRedirect(reverse('tos:terms_of_service-pending-terms', request=request))
        else:
            return Response(data={'detail': 'All pending terms accepted.'}, status=status.HTTP_202_ACCEPTED)

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'html':
            data = {'tos_list': self.get_queryset()}
            return Response(data)
        return super().list(request, *args, **kwargs)



