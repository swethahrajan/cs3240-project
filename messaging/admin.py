from django.contrib import admin
from .models import Message, Attachment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'body', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'file_size', 'get_message_display', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('file_name',)
    readonly_fields = ('file_size', 'file_type', 'uploaded_at')

    def get_message_display(self, obj):
        return f'{obj.message.sender} → {obj.message.recipient}'
    get_message_display.short_description = 'Message'

