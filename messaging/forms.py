from django import forms
from django.conf import settings
from .models import Message, Attachment


class MessageForm(forms.ModelForm):
    attachment = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': ','.join([f'.{ext}' for ext in settings.ALLOWED_FILE_EXTENSIONS])
        })
    )

    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 3,
                'style': 'resize: vertical;'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Message'

    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            # Check file size (25MB max)
            if attachment.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(
                    f'File size exceeds maximum allowed size of 25MB. Your file is {attachment.size / (1024*1024):.1f}MB.'
                )
            
            # Check file extension
            ext = attachment.name.split('.')[-1].lower()
            if ext not in settings.ALLOWED_FILE_EXTENSIONS:
                raise forms.ValidationError(
                    f'File type .{ext} is not allowed. Allowed types: {", ".join(settings.ALLOWED_FILE_EXTENSIONS)}'
                )
        return attachment
