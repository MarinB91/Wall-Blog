from django.contrib import admin
from .models import Message, CastedVotes

admin.site.register(Message)
admin.site.register(CastedVotes)