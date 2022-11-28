from django.urls import path, include
from .views import RoadMapListView, RoadMapDetailView

urlpatterns = [path('roadmap-list-view/', RoadMapListView, name = "roadmap-list-view"), path('roadmap-detail-view/<int:id>/', RoadMapDetailView, name = "roadmap-detail-view"),]