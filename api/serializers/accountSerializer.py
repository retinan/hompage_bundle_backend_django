from django.contrib.auth import get_user_model
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):
    username = serializers.EmailField(required=True, error_messages={
        'invalid': '유효한 이메일 주소를 입력해주세요.',
        'blank': '사용자의 이메일(Email)을 입력해주세요.',
    })
    password = serializers.CharField(required=True, error_messages={
        'blank': '비밀번호를 입력해주세요.',
    })

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError(_('계정이 비활성화 되었습니다.'))
                data['user'] = user
            else:
                raise serializers.ValidationError(_('이메일 또는 비밀번호가 틀립니다. 다시 입력해주세요.'))
        else:
            raise serializers.ValidationError(_('이메일과 비밀번호를 입력해주세요.'))
        return data


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.EmailField(required=True, error_messages={
        'invalid': '유효한 이메일 주소를 입력해주세요.',
        'blank': '본인의 이메일(Email)을 입력해주세요.',
    })
    password1 = serializers.CharField(required=True, error_messages={
        'blank': '비밀번호를 입력해주세요.',
    })
    password2 = serializers.CharField(required=True, error_messages={
        'blank': '비밀번호 확인을 입력해주세요.',
    })
    isCheck = serializers.BooleanField(required=True)

    def validate_username(self, value):
        print('validate_username ::: ', value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                _('이미 사용 중인 이메일(Email)입니다.'),
                code='unique'
            )
        return value

    def validate_password1(self, password):
        print('validate_password ::: ', password)
        # 비밀번호 규칙에 맞지 않을 때 에러 메시지 커스터마이징
        # 예시) 비밀번호는 최소 8자 이상, 숫자, 문자, 특수문자를 모두 포함해야 합니다.
        if len(password) < 8 or not any(char.isdigit() for char in password) or \
                not any(char.isalpha() for char in password) or not any(char.isalnum() for char in password):
            raise serializers.ValidationError(
                _("비밀번호는 최소 8자 이상, 숫자, 문자, 특수문자를 모두 포함해야 합니다."),
                code='password_too_weak'
            )
        return password

    def validate(self, data):

        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError(
                {'password2': _('비밀번호와 비밀번호 확인이 일치하지 않습니다.')},
                code='password_mismatch'
            )

        if not data.get('isCheck'):
            raise serializers.ValidationError(
                _('약관에 동의해주세요.'),
                code='missing_isCheck'
            )
        # username, email, password1, password2 validation
        super().validate(data)
        return data

