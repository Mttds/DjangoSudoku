from django.contrib import admin

# Register your models here.
from .models import Score # relative import from the models.py in this directory
admin.site.register(Score)
