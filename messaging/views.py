import mimetypes

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.views.decorators.http import require_http_methods

from .models import Message, Attachment
from .forms import MessageForm

User = None  # resolved lazily


def _get_user_model():
    global User
    if User is None:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    return User


def _conversation_response(request, other_user, form):
    """Build messages queryset, mark read, render conversation template."""
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user))
        | (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')
    messages.filter(
        sender=other_user, recipient=request.user, is_read=False
    ).update(is_read=True)
    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form,
    })


@login_required
def inbox(request):
    """List all users (except self) with unread message counts."""
    UserModel = _get_user_model()
    users = UserModel.objects.exclude(pk=request.user.pk).order_by('username')

    # Count unread messages per sender for the current user
    unread_counts = (
        Message.objects
        .filter(recipient=request.user, is_read=False)
        .values('sender')
        .annotate(count=Count('id'))
    )
    unread_map = {item['sender']: item['count'] for item in unread_counts}

    user_list = []
    for u in users:
        user_list.append({
            'user': u,
            'unread': unread_map.get(u.pk, 0),
        })

    return render(request, 'messaging/inbox.html', {'user_list': user_list})


@login_required
def conversation(request, user_id):
    """Show the chat history between the current user and another user."""
    UserModel = _get_user_model()
    other_user = get_object_or_404(UserModel, pk=user_id)

    form = MessageForm()
    return _conversation_response(request, other_user, form)


@login_required
@require_http_methods(["POST"])
def send_message(request, user_id):
    """Create a new message with optional file attachment."""
    UserModel = _get_user_model()
    other_user = get_object_or_404(UserModel, pk=user_id)
    
    form = MessageForm(request.POST, request.FILES)

    if not form.is_valid():
        return _conversation_response(request, other_user, form)

    message = Message.objects.create(
        sender=request.user,
        recipient=other_user,
        body=form.cleaned_data['body'] or '',
    )

    if 'attachment' in request.FILES:
        file = request.FILES['attachment']
        Attachment.objects.create(
            message=message,
            file=file,
            file_name=file.name,
            file_size=file.size,
            file_type=file.content_type or 'application/octet-stream',
        )

    return redirect('messaging:conversation', user_id=user_id)


@login_required
def download_attachment(request, attachment_id):
    """Download an attachment file."""
    attachment = get_object_or_404(Attachment, pk=attachment_id)
    message = attachment.message
    
    # Check permissions: user must be sender or recipient
    if request.user not in [message.sender, message.recipient]:
        return HttpResponseForbidden('You do not have permission to download this file.')

    inline = request.GET.get('inline') == '1'
    content_type = attachment.file_type or mimetypes.guess_type(attachment.file_name)[0]
    if not content_type:
        content_type = 'application/octet-stream'

    response = FileResponse(
        attachment.file.open('rb'),
        as_attachment=not inline,
        content_type=content_type,
    )
    disp = 'inline' if inline else 'attachment'
    response['Content-Disposition'] = f'{disp}; filename="{attachment.file_name}"'
    return response

