# coding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


from rest_framework import serializers


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):

    """
    Serializer for user login.
    Validates an email-password pair and authenticate it for login.
    """

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
        else:
            raise serializers.ValidationError(_('Invalid credentials.'))

        attrs['user'] = user
        return attrs


class UserEmailRegisterSerializer(serializers.Serializer):

    """
    Serializer for user registration.
    Creates a user instance.
    """

    fname = serializers.CharField()
    lname = serializers.CharField()
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField()
    password = serializers.CharField(required=False, allow_blank=True)
    provider = serializers.CharField(required=False, allow_blank=True)
    access_token = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ('fname','lname','phone','email','password','provider','access_token')


    def __init__(self, *args, **kwargs):
        super(UserEmailRegisterSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        has_provider = data.get('provider')
        password = data.get('password')
        email = data.get('email')
        if not has_provider:
            if not password or password == '':
                raise serializers.ValidationError(_('Password should not be empty.'))

        try:
            User.objects.get(email=email)
            raise serializers.ValidationError(_('User with this email already exists.'))
        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        validated_data.update({
            'username':validated_data['email']
        })
        user = User.objects.create(username=validated_data['username'],
                                   first_name=validated_data['fname'],
                                   last_name=validated_data['lname'],
                                   email=validated_data['email'],
                                   mobile=validated_data.get('phone',None))
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving user profile details.
    """

    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'fname', 'lname','email','role', 'phone', 'address')

    def get_fname(self, obj):
        return '%s'%(obj.first_name)

    def get_lname(self, obj):
        return '%s'%(obj.last_name)

    def get_phone(self, obj):
        return '%s'%(obj.mobile) if obj.mobile else ''

    def get_address(self, obj):
        return ""

