from django.contrib import admin
from .models import RoadMap
from django_summernote.admin import SummernoteModelAdmin


class RoadMapAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    summernote_fields = ('desc',)
    search_fields = ('user__username',)



# Register your models here.
admin.site.register(RoadMap, RoadMapAdmin)