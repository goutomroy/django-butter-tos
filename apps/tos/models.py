from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

DEFAULT_TERMS_SLUG = "butter-tos"
TERMS_CACHE_SECONDS = 60


class UserTermsOfService(models.Model):
    """Holds mapping between TermsofService and Users"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    terms = models.ForeignKey("TermsOfService", on_delete=models.CASCADE)
    profile_at_moment = JSONField(blank=True, editable=False,
                                         help_text=_("User profile data at the moment of agreement sign."))
    date_accepted = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Accepted"), editable=False)

    class Meta:
        default_related_name = 'user_terms'
        get_latest_by = "date_accepted"
        verbose_name = _("User Terms of Service")
        verbose_name_plural = _("User Terms of Service")
        constraints = [
            models.UniqueConstraint(fields=['user', 'terms'], name='Unique user terms')
        ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            from apps.main.serializers import UserProfileSerializer
            # user_profile = UserProfile.objects.get(user=self.user)
            self.profile_at_moment = UserProfileSerializer(self.user.user_profile).data
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.get_username()}:{self.terms.slug}-{self.terms.version_number}"


class TermsOfService(models.Model):

    slug = models.SlugField(default=DEFAULT_TERMS_SLUG)
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through=UserTermsOfService, blank=True)
    version_number = models.DecimalField(default=1.0, decimal_places=2, max_digits=6)
    text = models.TextField(help_text=_("Main terms of services text"))
    info = models.TextField(help_text=_("Provide users with some info about what's changed and why"))
    status = models.BooleanField(default=False)
    activation_date = models.DateTimeField(help_text=_("When this TOS will be active"))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        default_related_name = 'terms_of_services'
        verbose_name = "Terms of Service"
        verbose_name_plural = "Terms of Services"

    @staticmethod
    def get_pending_terms(user: settings.AUTH_USER_MODEL):
        pending_terms = cache.get(f"pending_terms_{user.id}")
        if not pending_terms:
            pending_terms = TermsOfService.objects.filter(status=True, activation_date__lte=timezone.now())\
                .exclude(user_terms__in=UserTermsOfService.objects.filter(user=user))\
                .defer('users', 'created', 'updated')\
                .order_by('activation_date', '-version_number')
            if pending_terms.exists():
                logger.info(f"pending_terms query : {pending_terms.query}")
                cache.set(f"pending_terms_{user.id}", pending_terms, TERMS_CACHE_SECONDS)
                logger.info(f"pending_terms_cache : {pending_terms._result_cache} type: {type(pending_terms)}")
        return pending_terms

    def get_absolute_url(self):
        return reverse("tos:terms_of_service-detail", args=[self.id])

    def __str__(self):
        return f"{self.slug}-{self.version_number}"


