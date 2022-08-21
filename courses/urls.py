from django.urls import path, include

from .views import CourseListView, CourseDetailView, CourseSearchView, AllCourseView


urlpatterns = [

    path('courses-list-view/', CourseListView, name = "courses-list-view"),
    path('courses-detail-view/<int:id>/', CourseDetailView, name = "courses-detail-view"),
    path('courses-search-view/<str:tag>/', CourseSearchView, name = "courses-search-view"),
    path('all-courses-view/', AllCourseView, name = "all-courses-view"),

]