from rest_framework import viewsets
from apps.main.models import UserProfile
from apps.main.serializers import UserProfileSerializer
from apps.tos.decorators import terms_checker


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    tos_slugs = ['site-terms']

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

    @terms_checker
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)