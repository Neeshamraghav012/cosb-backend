from django.contrib import admin
from .models import Course, Ratings
# Register your models here.

from django_summernote.admin import SummernoteModelAdmin


class CourseAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Ratings)