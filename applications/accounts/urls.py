# coding=utf-8

from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from applications.accounts import views as account_view

from utils.decorators import check_authorized

router = DefaultRouter()

urlpatterns = [

    url(r'^login/$', account_view.UserLoginView.as_view(), name='user-login'),
    url(r'^register/$', account_view.UserEmailRegisterView.as_view(), name='user-email-register'),
    url(r'^logout/$', check_authorized(account_view.UserLogoutView.as_view()), name='user-logout'),
    url(r'^session-status/$', account_view.UserSessionStatusView.as_view(), name='user-session-status'),
    # url(r'^check-email/$', account_view.CheckEmailView.as_view(), name='check-email'),
    # url(r'^account/$', check_authorized(account_view.UserProfileDetail.as_view()), name='user-profile'),
    # url(r'^reset-password/$', account_view.PasswordResetView.as_view(), name='user-password-reset'),
    # url(r'^update-password/$', account_view.PasswordUpateView.as_view(), name='user-password-update'),

    url(r'^devices/register/$', csrf_exempt(account_view.RegisterDevice.as_view()), name='register-mobile-device'),
    url(r'^ad/stores/(?P<store_id>\d+)/iamhere/$', account_view.ArrivalDetectionView.as_view(), name='user-ad'),

    url(r'^', include(router.urls)),

]
