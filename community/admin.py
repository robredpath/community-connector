from django.contrib import admin

# Register your models here.
from community.models import Message, Event

admin.site.register(Message)
admin.site.register(Event)