from django.contrib import admin
from .models import TestApp,Relate, Poll, Choice, Vote
# Register your models here.
admin.site.register((TestApp, Relate, Poll, Choice, Vote))