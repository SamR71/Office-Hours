# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Todo 

class TodoAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'completed')

# Register your models here.
admin.site.register(Todo, TodoAdmin)
