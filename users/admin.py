from django.contrib import admin
from .models import Conversation,ConversationMessages

admin.site.register(Conversation)
admin.site.register(ConversationMessages)