# coding=utf-8

from django.contrib.auth import login, logout
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response


from utils.helpers import ErrorType
from utils.csrf import UnsafeSessionAuthentication
from applications.accounts.auth import MyAPISignatureAuthentication
from applications.accounts.serializer import UserLoginSerializer, UserEmailRegisterSerializer, \
    UserProfileSerializer
from applications.accounts.models import Device, ArrivalDetection


class UserEmailRegisterView(APIView, ErrorType):

    """
    Performs User registration using email user filled profile details.
    """

    serializer_class = UserEmailRegisterSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.UserEmailRegisterSerializer


        """
        response = dict(status='success')

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
                user = serializer.create(serializer.validated_data)
                return Response(data=UserProfileSerializer(instance=user).data)

        return Response(serializer.errors, status=self.BAD_REQUEST)


class UserLoginView(APIView, ErrorType):
    """
    Performs login action on given values for email and password.

    """

    serializer_class = UserLoginSerializer

    def post(self, request, format=None):

        """
        Request Methods : [POST]
        ---

        serializer: applications.accounts.serializer.UserLoginSerializer


        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            if user is not None and user.is_active:
                login(request, user)
                return Response(response)

        return Response(serializer.errors, status=self.NOT_AUTHORIZED)


class UserLogoutView(APIView):
    """
    Performs logout action for an authenticated request.

    """

    def post(self, request, format=None):
        """
        Request Methods : [POST]
        ---

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated


        """
        response = dict(status='success')
        if request.user.is_authenticated():
            logout(request)
        return Response(response)


class UserSessionStatusView(APIView):
    """
    Validates a user session status.

    Request Methods : [GET]
    """

    def get(self, request, format=None):
        """
        ---
        type:
          logged-in:
            required: true
            type: boolean

        """
        return Response({"logged-in":request.user.is_authenticated()})


class RegisterDevice(APIView, ErrorType):
    """
    API view to register an Android/IOS device.
    """

    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, request, *args, **kwargs):
        response = Response(data={"status": False})
        ua = request.META.get('HTTP_X_CLIENT_DEVICE', '').lower()
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        print user_agent
        token_updated = False
        if ua == "android":
            deviceID = self.request.data.get('udid')
            registrationID = self.request.data.get('push_token')

            if not deviceID or not registrationID:
                return Response(status=self.MISSING_ATTRIBUTES)
            device, created = Device.objects.get_or_create(device_id=deviceID)

            # Check the user is authenticated
            if request.user.is_authenticated():
                device.user = request.user
                devices = Device.objects.filter(user=request.user).exclude(device_id=deviceID)
                if devices:
                    # Deleting other devices associated with this user
                    # This is incorrect. We need to update these devices with empty user
                    devices.objects.all().update(user=None)
                    # devices.delete()
            else:
                device.user = None

            # update with current registration_id if it is not set
            if not device.registration_id:
                device.registration_id = registrationID
                device.save()

            # if device existing and registration id changed > Update SNS ARN
            if not device.registration_id == registrationID and not created:
                if device.aws_subscription_arn:
                    self.update_sns_endpoint(device.aws_subscription_arn, registrationID, device)
                device.registration_id = registrationID
                device.save()

            # if the device is new
            if not device.aws_subscription_arn:
                self.create_sns_endpoint(registrationID, device)

            user_agent_data = user_agent.split('/') if user_agent else []
            if len(user_agent_data) == 3:
                user_agent_data[1] = user_agent_data[1].replace('android Android', '')
                device.version = user_agent_data[1]
                device.device_info = user_agent_data[2]
            else:
                device.version = user_agent
            device.save()
            return Response(status=self.SUCCESS)

        if ua.find("iphone") > 0:
            # TODO:Detect and add data for IOS device
            pass

        return Response(status=self.NOT_FOUND)

    def create_sns_endpoint(self, token, device):
        return True

    def update_sns_endpoint(self, old_arn, new_token, device):

        return True


class ArrivalDetectionView(APIView, ErrorType):
    """
    Update user analytics data
    """

    # authentication_classes = (UnsafeSessionAuthentication,)
    authentication_classes = (MyAPISignatureAuthentication,)

    def post(self, request, store_id, *args, **kwargs):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_id = request.META.get('HTTP_X_DEVICE_ID', '')

        # user_agent = request.POST.get('HTTP_USER_AGENT', '')
        # device_id = request.POST.get('HTTP_X_DEVICE_ID', '')

        if device_id:
            try:
                analytics, created = ArrivalDetection.objects.get_or_create(device_id=device_id, store=store_id)
            except ArrivalDetection.MultipleObjectsReturned:
                all_analytics = ArrivalDetection.objects.filter(device_id=device_id, store=store_id)
                analytics = all_analytics[0]
                created = False
                duplicates = all_analytics[1:]
                for item in duplicates:
                    item.delete()

            if not created:
                analytics.date = timezone.now()
            if request.user.is_authenticated():
                analytics.user = request.user
            user_agent_data = user_agent.split('/') if user_agent else []
            if len(user_agent_data) == 3:
                user_agent_data[1] = user_agent_data[1].replace('android', '')
                analytics.version = user_agent_data[1]
                analytics.device_info = user_agent_data[2]
            else:
                analytics.version = user_agent
            analytics.save()
            return Response(status=self.SUCCESS)
        else:
            return Response(status=self.MISSING_ATTRIBUTES)