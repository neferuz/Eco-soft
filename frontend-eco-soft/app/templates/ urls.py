from django.shortcuts import render
from django.urls import path
from .views import contacts_html

def contacts(request):
    return render(request, 'contacts.html')

urlpatterns = [
    path('contacts.html', contacts_html, name='contacts_html'),
]
