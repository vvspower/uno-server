from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerialzier
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from .utils import upload_profile_picture, get_user_from_request
from rest_framework_simplejwt.authentication import JWTAuthentication

JWT_authenticator = JWTAuthentication()


# Create your views here.

@api_view(["POST"])
def RegisterUser(request):
    serializer = UserSerialzier(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(**serializer.validated_data, avatar=upload_profile_picture(request.data["username"]))
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
        "refresh": str(refresh), 'access': str(refresh.access_token)})
    else:
        return Response(serializer.errors)
    

@api_view(["POST"])
def LoginUser(request):
    try:
        user = get_user_from_request(request)
        serializer = UserSerialzier(user)
        return Response(serializer.data)
    except Exception as ex:
        return Response(ex.args[0], status=400)


@api_view(["GET"])
def GetUser(request, pk):
    try:
        user = User.objects.get(id=pk)
        if user is not None:
            serializer = UserSerialzier(user)
            return Response(serializer.data)
        else:
            return Response({"msg" : "user not found"}, status=404)
    except Exception as ex:
        return Response(ex.args[0], status=400)



