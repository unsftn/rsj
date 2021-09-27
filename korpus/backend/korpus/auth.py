from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    Uses email instead of username for authentication.
    """
    def authenticate(self, request, username=None, password=None):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id)
        except user_model.DoesNotExist:
            return None
        else:
            return user
