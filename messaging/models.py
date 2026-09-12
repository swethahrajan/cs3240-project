from django.db import models
from django.conf import settings
import os


def message_attachment_path(instance, filename):
    """Generate file path for message attachments: messaging/<sender_id>/<recipient_id>/<filename>"""
    return f'messaging/{instance.message.sender.id}/{instance.message.recipient.id}/{filename}'


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender} → {self.recipient}: {self.body[:50]}'


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=message_attachment_path)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()  # In bytes
    file_type = models.CharField(max_length=50)  # MIME type
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.file_name} ({self.get_file_size_display()})'

    def get_file_size_display(self):
        """Convert bytes to human-readable format"""
        n = float(self.file_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if n < 1024:
                return f'{n:.1f} {unit}'
            n /= 1024
        return f'{n:.1f} TB'

    def get_file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.file_name)[1].lower().strip('.')

    def is_image(self):
        """Check if file is an image"""
        image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
        return self.get_file_extension() in image_extensions

    def is_pdf(self):
        """Check if file is a PDF"""
        return self.get_file_extension() == 'pdf'

