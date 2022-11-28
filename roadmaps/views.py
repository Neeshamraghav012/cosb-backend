from .serializers import RoadMapSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import RoadMap
import json

# Customizable Function based view.
@api_view(['GET'])
def RoadMapListView(request):


   snippet = RoadMap.objects.all()
   serializer = RoadMapSerializer(snippet, many = True)
   return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def RoadMapDetailView(request, id):

    if request.method == 'GET':

        try:
            snippet = RoadMap.objects.get(id = id)
            serializer = RoadMapSerializer(snippet)
            return JsonResponse(serializer.data, safe=False)

        except:
            return JsonResponse({status: 0})