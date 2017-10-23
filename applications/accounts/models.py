from __future__ import unicode_literals


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_extensions.db.fields import ModificationDateTimeField


from utils.constants import USER_ROLES, BECO_CUSTOMER


class User(AbstractUser):

    """ Custom user model for every beco user. """

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )

    mobile = models.CharField(_('Mobile Number'), max_length=25, null=True, blank=True)
    gender = models.CharField(_('Gender'), choices=GENDER_CHOICES, max_length=25, null=True, blank=True)
    dob = models.DateField(verbose_name=_('DOB'), null=True, blank=True)
    role = models.CharField(_('Role'), choices=USER_ROLES, max_length=25, default=BECO_CUSTOMER)
    api_key = models.CharField(_('API KEY'), max_length=25, blank=True, null=True)
    secret_key = models.CharField(_('Secret String'), max_length=25, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return self.get_username()


class Device(models.Model):
    """
    Abstract base model for mobile device data.
    """
    active = models.BooleanField(
        verbose_name=_("Is active"), default=True,
        help_text=_("Inactive devices will not be sent notifications")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    date_created = models.DateTimeField(
        verbose_name=_("Creation date"), auto_now_add=True, null=True
    )

    date_modified = ModificationDateTimeField(_('Modified date'))

    device_id = models.TextField(
        verbose_name=_("Device ID"), db_index=True,
        help_text=_("ANDROID_ID / TelephonyManager.getDeviceId() (always as hex)")
    )
    registration_id = models.TextField(verbose_name=_("Registration ID"), blank=True, null=True)
    aws_subscription_arn = models.TextField(verbose_name=_("AWS Topic Subscription ARN"), blank=True, null=True)
    version = models.TextField(verbose_name=_("APP Version"), blank=True, null=True)
    device_info = models.TextField(verbose_name=_("Device Info"), blank=True, null=True)

    class Meta:
        verbose_name = _("GCM device")

    def __str__(self):
        return (
            "%s for %s" % (self.__class__.__name__, self.user or "unknown user")
        )


class ArrivalDetection(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='user_arrivaldetection', null=True, blank=True)
    store = models.TextField(verbose_name=_('Store'))
    device_id = models.TextField(
        verbose_name=_("Device ID"), db_index=True,
        help_text=_("ANDROID_ID / TelephonyManager.getDeviceId() (always as hex)")
    )
    date = models.DateTimeField(_('Date'), default=timezone.now)
    version = models.TextField(verbose_name=_("APP Version"), blank=True, null=True)
    device_info = models.TextField(verbose_name=_("Device Info"), blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Arrival Detections')

    def __unicode__(self):
        return unicode(self.device_id)
