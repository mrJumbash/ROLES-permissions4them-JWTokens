from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserService:
    __user_model = User

    @staticmethod
    def tokens(user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
