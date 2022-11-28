
from django.contrib import admin
from django.urls import path, include

from courses import urls as courses_urls
from users import urls as user_urls
from roadmaps import urls as roadmap_urls
from users.views import GoogleLoginApi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/courses/', include(courses_urls)),
    path('api/user/', include(user_urls)),
    path('api/roadmaps/', include(roadmap_urls)),
    path('api/v1/auth/login/google/', GoogleLoginApi.as_view(), name = 'google_login'),
    path('summernote/', include('django_summernote.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)