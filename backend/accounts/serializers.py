# backend/accounts/serializers.py
from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username  = serializers.CharField(max_length=150)
    email     = serializers.EmailField()
    password  = serializers.CharField(write_only=True, trim_whitespace=False)
    password2 = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("username_taken")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("email_taken")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "password_mismatch"})
        # Reglas de seguridad de Django (fuerza mínima, etc.)
        password_validation.validate_password(data["password"])
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
