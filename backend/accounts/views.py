# backend/accounts/views.py
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .serializers import RegisterSerializer
from shop.utils import merge_guest_cart_to_user
import logging

class Ping(APIView):
    def get(self, request):
        return Response({"message": "pong"})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class Csrf(APIView):
    def get(self, request):
        return Response({"detail": "ok"})

class Register(APIView):
    permission_classes = [AllowAny]  # público, pero CSRF sigue aplicando
    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=400)
        user = s.save()
        login(request, user)  # auto-login tras registrar
        return Response({"detail": "registered", "username": user.username}, status=201)

logger = logging.getLogger(__name__)

class Login(APIView):
    def post(self, request):
        data = request.data or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response({"detail": "missing_fields"}, status=400)

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "invalid_credentials"}, status=400)

        login(request, user)

        # <-- FUSIÓN DE CARRITO INVITADO -> USUARIO
        try:
            merged = merge_guest_cart_to_user(request, user)
            # Si quieres devolver info del merge, descomenta:
            # return Response({"detail": "logged", **merged})
        except Exception as e:
            logger.exception("Cart merge failed: %s", e)

        return Response({"detail": "logged"})

class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "logged_out"})

class Me(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "authenticated": True,
                "username": request.user.username,
                "email": request.user.email,
                "is_staff": request.user.is_staff,  # <-- importante
            })
        return Response({"authenticated": False})


