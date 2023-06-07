from rest_framework import serializers
from social_auth.services import GoogleService
from social_auth.utils import register_social_user
from rest_framework.exceptions import AuthenticationFailed


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = GoogleService.validate(auth_token)
        print(user_data)
        try:
            user_data["sub"]
        except:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
