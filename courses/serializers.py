from dataclasses import fields
from rest_framework import serializers

from .models import Course, Ratings

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ratings
        fields = "__all__"
        depth = 1