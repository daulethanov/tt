import random
import re
from rest_framework import serializers as s
from api import code_dict


class AuthSerializer(s.Serializer):
    numbers = s.CharField(min_length=5, max_length=12)

    def validate_numbers(self, value):
        if not re.match(r'^\+\d+$|^\d+$', value):
            raise s.ValidationError("В поле numbers допустимы только цифры и символ '+' в начале строки.")
        return value

    def generate_code(self):
        code = random.randint(1000, 9999)
        code_dict[code] = self.validated_data['numbers']
        return code


class CodeSerializer(s.Serializer):
    code = s.IntegerField()

    def validate_numbers(self, value):
        if not (1000 <= value <= 9999):
            raise s.ValidationError("Поле numbers должно быть четырехзначным числом.")
        return value


class InviteSerializer(s.Serializer):
    invite_code = s.CharField()


class UserSerializer(s.Serializer):
    invite_code = s.CharField()
    numbers = s.CharField()


class ProfileSerializer(s.Serializer):
    numbers = s.CharField()
    code = s.CharField()


class AllNumberInvited(s.Serializer):
    numbers = s.ListField(child=s.CharField())