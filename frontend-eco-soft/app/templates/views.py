from django.shortcuts import render

def contacts_html(request):
    return render(request, 'contacts.html')

urlpatterns = [
    # ... другие маршруты ...
    path('contacts.html', contacts_html, name='contacts_html'),
]