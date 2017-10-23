from rest_framework_httpsignature.authentication import SignatureAuthentication

from applications.accounts.models import User


class MyAPISignatureAuthentication(SignatureAuthentication):
    # The HTTP header used to pass the consumer key ID.
    # Defaults to 'X-Api-Key'.
    API_KEY_HEADER = 'X-Api-Key'

    # A method to fetch (User instance, user_secret_string) from the
    # consumer key ID, or None in case it is not found.
    def fetch_user_data(self, api_key):
        # ...
        # example implementation:
        try:
            import ipdb; ipdb.set_trace();
            user = User.objects.get(api_key=api_key)
            return (user, user.secret)
        except User.DoesNotExist:
            return None
