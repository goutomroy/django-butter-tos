import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.main.models import UserProfile
from apps.main.paginations import StandardResultsSetPagination
from apps.main.serializers import UserProfileSerializer
from apps.tos.decorators import terms_checker

logger = logging.getLogger(__name__)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserProfile.objects.select_related('user').all()

    def get_template_names(self):
        app = self.request.resolver_match.app_name
        templates = {
            'list': [f"{app}/list.html", "list.html"],
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

    @terms_checker
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @terms_checker
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @terms_checker
    @action(methods=['get'], detail=False)
    def email_list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            email_list = [{'user_id': each.user.id, 'email': each.user.email} for each in page]
            return self.get_paginated_response(email_list)

        email_list = [{'user_id': each.user.id, 'email': each.user.email} for each in page]
        return Response(email_list)
