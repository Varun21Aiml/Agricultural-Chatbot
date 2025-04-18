# agricultural_chatbot/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),  # 👈 Includes chatbot URLs as homepage
]
