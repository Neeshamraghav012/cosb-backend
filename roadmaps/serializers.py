from dataclasses import fields
from rest_framework import serializers

from .models import RoadMap

class RoadMapSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoadMap
        fields = "__all__"
        depth = 2
