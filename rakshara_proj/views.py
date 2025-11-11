from django.shortcuts import redirect
from django.utils import translation

def set_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language', 'en')
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        translation.activate(lang)
        return redirect('home')
