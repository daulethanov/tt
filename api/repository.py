from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from api import code_dict
from api.models import User


class AuthRepository:

    @classmethod
    def generate_token(cls, user) -> str:
        token = AccessToken.for_user(user)
        return str(token)

    @staticmethod
    def create_user(code: int) -> str:
        if code in code_dict:
            number = code_dict[code]
            try:
                user = User.objects.get(numbers=number)
                del code_dict[code]
                token = AuthRepository.generate_token(user)
                return token
            except User.DoesNotExist:
                user = User.objects.create(numbers=number)
                user.generate_code()
                user.save()
                token = AuthRepository.generate_token(user)
                del code_dict[code]
                return token
        else:
            raise ValidationError("Такого кода нет")

    @staticmethod
    def view_account(user_id) -> dict:
        user = User.objects.get(id=user_id)
        if user:
            res = {
                "numbers": user.numbers,
                "code": user.code
            }
            return res
        else:
            return {"error": "Такого юзера нет"}


class LinkInviteRepository:
    @staticmethod
    def link_user_code(code, user_id) -> dict:
        user = User.objects.get(id=user_id)
        if user:
            invite_user = User.objects.filter(code=code).first()
            if invite_user:
                if user.invite_profile == code:
                    return {
                        "invite_code": invite_user.code,
                        "numbers": invite_user.numbers
                    }
                else:
                    user.invite_profile = code
                    user.save()
                    return {"ok": "success"}
            else:
                return {"error": "Такого юзера нет"}

    @staticmethod
    def all_user_invited(user_id):
        user = User.objects.get(id=user_id)
        if user:
            invited_users = user.invite_profile
            all_user_data = User.objects.filter(invite_profile=invited_users).values("numbers")
            numbers_list = []

            for data in all_user_data:
                numbers_list.append(data["numbers"])
            return numbers_list
