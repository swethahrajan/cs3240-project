from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:user_id>/', views.conversation, name='conversation'),
    path('<int:user_id>/send/', views.send_message, name='send_message'),
    path('attachment/<int:attachment_id>/download/', views.download_attachment, name='download_attachment'),
]
