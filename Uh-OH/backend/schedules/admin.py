from django.contrib import admin
from .models import userScheduleItem, userSchedules
# Register your models here.
admin.site.register(userScheduleItem)
admin.site.register(userSchedules)