from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from account.serializers import RegisterSerializer
from account.models import User

from django.contrib.auth import authenticate


class LoginAPIView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                token,created = Token.objects.get_or_create(user=user)
                return Response({'token':token.key})
            else:
                return Response(data={'error':'invalid user credential'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT,data={'error':'email or password required'})


class RegistrationAPIView(APIView):

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class VerifyUser(APIView):

    def post(self,request,email,code):

        if User.objects.filter(email=email,is_active=False,verify=code):
            data = {}
            user = User.objects.get(email=email)
            user.is_active = True
            user.verify = 0
            user.save()

            Token.objects.create(user=user)
            token = Token.objects.get(user=user).key
            data['email'] = user.email
            data['name'] = user.name
            data['token'] = token
            return Response(status=status.HTTP_202_ACCEPTED, data=data)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            

class LogoutAPIView(APIView):

    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



