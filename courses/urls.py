from django.urls import path, include

from .views import CourseListView, CourseDetailView, CourseSearchView


urlpatterns = [

    path('courses-list-view/', CourseListView, name = "courses-list-view"),
    path('courses-detail-view/<int:id>/', CourseDetailView, name = "courses-detail-view"),
    path('courses-search-view/<str:tag>/', CourseSearchView, name = "courses-search-view"),



]