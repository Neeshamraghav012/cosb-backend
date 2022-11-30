from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from users.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer, CourseStatusSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CourseStatus
from rest_framework import permissions
import json
import jwt
from myapp.settings import SECRET_KEY
from courses.models import Course
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from urllib.parse import urlencode
from django.db import transaction
from rest_framework import status, serializers
from rest_framework.views import APIView

from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.urls import reverse
from django.conf import settings

from .mixins import ApiErrorsMixin, PublicApiMixin, ApiAuthMixin


from .services import jwt_login, google_get_access_token, google_get_user_info


def user_create(email, username, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        **extra_fields
    }

    user = User(email=email, username=username, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, username: str, email: str, **extra_data):
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, username=username, **extra_data), True

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):


    def post(self, request, format='json'):
        
        print(request.data)
        serializer = RegisterSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status": 1})

        return JsonResponse(serializer.errors, status = 400)




@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/'
    ]
    return Response(routes)


# Only for testing
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def testEndPoint(request):
    if request.method == 'GET':
        data = f"Congratulation {request.user}, your API just responded to GET request"
        return Response({'response': data}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        text = request.POST.get('text')
        data = f'Congratulation your API just responded to POST request with text: {text}'
        return Response({'response': data}, status=status.HTTP_200_OK)
    return Response({}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def StatusView(request):

    reqBody = json.loads(request.body)
    json_token = reqBody['token']
    data = jwt.decode(json_token, SECRET_KEY, algorithms=['HS256'])
    user = User.objects.get(username = data['username'])
    course = Course.objects.get(id = reqBody['id'])


    check = CourseStatus.objects.filter(user = user, course = course)

    if check:
        for i in check:
            i.delete()


    status = CourseStatus(user = user, course = course, status = reqBody['status'])
    status.save()
    return JsonResponse({"status": 1})


@api_view(['GET', 'POST'])
def cosbid(request):

    reqBody = json.loads(request.body)

    username = reqBody['username']

    users = User.objects.filter(username__istartswith = username)

    serializer = UserSerializer(users, many = True)

    return JsonResponse(serializer.data, safe=False)



@api_view(['GET', 'POST'])
def profileView(request):

    reqBody = json.loads(request.body)
    username = reqBody['username']

    try:

        user = User.objects.get(username = username)
        courses = CourseStatus.objects.filter(user = user)

        serializer = CourseStatusSerializer(courses, many=True)
        return JsonResponse(serializer.data, safe=False)



    except Exception as e:

        print(e)
        return JsonResponse({"status": 0})




@api_view(['GET'])
def profileViewByName(request, username):


    try:

        user = User.objects.get(username = username)
        courses = CourseStatus.objects.filter(user = user)
        serializer = CourseStatusSerializer(courses, many = True)
        return JsonResponse(serializer.data, safe=False)


    except Exception as e:

        print(e)
        return JsonResponse({"status": 0})



class GoogleLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'https://cosb.online/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        #domain = 'http://127.0.0.1:8000/api/v1/auth/login/google/'
        #api_uri = reverse('api:v1:auth:login-with-google')

        redirect_uri = 'https://cosbapi.herokuapp.com/api/v1/auth/login/google/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        print("".join(user_data['name'].split(' ')))

        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('givenName', ''),
            'last_name': user_data.get('familyName', ''),
            'username': "".join(user_data['name'].split(' ')),
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**profile_data)


        json_data = {"email": profile_data['email']}

        token = jwt.encode(payload=json_data, key=SECRET_KEY, algorithm="HS256")
        response = redirect(f"https://cosb.online?token={token}&username={profile_data['username']}")
        response = jwt_login(response=response, user=user)

        # response.set_cookie('token', jwt.encode(payload=json_data, key=SECRET_KEY, algorithm="HS256"))
        # print(request.COOKIES.get('token', 'Nothing in cookie'))


        return response