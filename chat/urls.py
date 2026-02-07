from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_page, name='chatbot_page'),
    path('send-message/', views.send_chat_message, name='send_chat_message'),
]
