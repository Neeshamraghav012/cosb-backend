from django.shortcuts import render
from .serializers import CourseSerializer, ReviewSerializer
from django.http import HttpResponse, JsonResponse
from .models import Course, Ratings
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
import json
import jwt
from myapp.settings import SECRET_KEY
from rest_framework import permissions

# Customizable Function based view.
@api_view(['GET'])
def CourseListView(request):


   reqBody = json.loads(request.body)
   count = int(reqBody["count"])
   
   snippet = Course.objects.all()[count:(count + 5)]
   if request.method == 'GET':
      serializer = CourseSerializer(snippet, many = True)
      return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def AllCourseView(request):
   
   snippet = Course.objects.all()
   if request.method == 'GET':
      serializer = CourseSerializer(snippet, many = True)
      return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def CourseDetailView(request, id):

    if request.method == 'GET':

        try:
            snippet = Course.objects.get(id = id)
            serializer = CourseSerializer(snippet)
            return JsonResponse(serializer.data, safe=False)

        except:
            return JsonResponse({status: 0})


@api_view(['GET'])
def CourseSearchView(request, tag):
   
   tag = tag.lower().split(' ')
   print(tag)
   snippet = Course.objects.filter(tags__name__in = tag)[:5]

   if request.method == 'GET':
      serializer = CourseSerializer(snippet, many = True)
      return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def RateView(request):

   reqBody = json.loads(request.body)
   json_token = reqBody['token']
   data = jwt.decode(json_token, SECRET_KEY, algorithms=['HS256'])

   user = User.objects.get(username = data['username'])
   course = Course.objects.get(id = reqBody['id'])

   check = Ratings.objects.filter(user = user)

   if check:
      for i in check:
         i.delete()


   rating = Ratings(user = user, course = course, rating = float(reqBody['rating']), review = reqBody['review'])
   rating.save()
   rating.update_rating()
   return JsonResponse({"status": 1})


@api_view(['POST'])
def TestToken(request):

   reqBody = json.loads(request.body)
   json_token = reqBody['token']

   try:
      data = jwt.decode(json_token, SECRET_KEY, algorithms=['HS256'])
      return JsonResponse(data)


   except:

      return JsonResponse({"status": 0})





@api_view(['GET'])
def Reviews(request):

   reqBody = json.loads(request.body)
   course_id = reqBody["id"]

   try:

      course = Course.objects.get(id = course_id)
      reviews = Ratings.objects.filter(course = course)
      serializer = ReviewSerializer(reviews, many = True)
      return JsonResponse(serializer.data, safe=False)

   except Exception as e:

      print(e)
      return JsonResponse({"status": 0})

