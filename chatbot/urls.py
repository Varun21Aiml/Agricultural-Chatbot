# chatbot/urls.py

from django.urls import path
from .views import chatbot_ui, chatbot_response

urlpatterns = [
    path('', chatbot_ui, name='chatbot_ui'),  # Shows the HTML page
    path('get-response/', chatbot_response, name='chatbot_response')  # Handles user input
]
