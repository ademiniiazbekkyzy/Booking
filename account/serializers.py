from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

# from applications.account.send_mail import send_mail_message
from account.models import MyUser
from account.send_mail import send_activation_code
# from booking_api.tasks import send_mail_message

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):  # validate_password ?
        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm')  # почему get-Error | pop норм
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого email не существует')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = "Must include email and password"
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


# class CustomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('date_joined', 'email', 'is_active', 'is_superuser')
#
#
# class ForgotSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError('неверный Emial')
#         return email
#
#     def send_code(self):
#         email = self.validated_data.get('email')
#         user = User.objects.get(email=email)
#         user.create_activation_code()
#         user.save()
#         send_mail_message.delay(email=user.email, code=user.activation_code, status='reset_password')
#
#
# class ForgotCompleteSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True, min_length=6)
#     password2 = serializers.CharField(required=True, min_length=6, write_only=True)
#     activation_code = serializers.CharField(required=True)
#
#     def validate_email(self, email):
#         if not User.objects.filter(email=email).exists():
#             raise serializers.ValidationError("Пользователь не найден")
#         return email
#
#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.pop('password2')
#
#         if password != password2:
#             raise serializers.ValidationError('Пароли не совпадают')
#
#         code = attrs.get('activation_code')
#         if not User.objects.filter(activation_code=code).exists():
#             raise serializers.ValidationError('Неверный активационный код')
#         return attrs
#
#     def set_new_password(self):
#         email = self.validated_data.get('email')
#         password = self.validated_data.get('password')
#         user = User.objects.get(email=email)
#         user.set_password(password)
#         user.activation_code = ''
#         user.save()
#
