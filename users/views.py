from django.shortcuts import render
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




"""
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

"""


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

