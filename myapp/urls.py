
from django.contrib import admin
from django.urls import path, include

from courses import urls as courses_urls
from users import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/courses/', include(courses_urls)),
    path('api/user/', include(user_urls)),

]


