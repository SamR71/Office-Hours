from django.contrib import admin
from .models import UserScheduleItem, UserSchedules
# Register your models here.
admin.site.register(UserScheduleItem)
admin.site.register(UserSchedules)