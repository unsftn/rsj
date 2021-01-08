from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RichTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['email'] = self.user.email
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['user_id'] = self.user.id
        data['is_staff'] = self.user.is_staff
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data


class RichTokenObtainPairView(TokenObtainPairView):
    serializer_class = RichTokenObtainPairSerializer
