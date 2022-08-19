from django.shortcuts import render
from .serializers import CourseSerializer
from django.http import HttpResponse, JsonResponse
from .models import Course
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import JSONParser

# Customizable Function based view.
@api_view(['GET'])
def CourseListView(request):
   
   snippet = Course.objects.all()[:50]
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
   snippet = Course.objects.filter(tags__name__in = tag)

   if request.method == 'GET':
      serializer = CourseSerializer(snippet, many = True)
      return JsonResponse(serializer.data, safe=False)

