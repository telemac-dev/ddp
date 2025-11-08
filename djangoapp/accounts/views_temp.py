from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

@login_required
def temp_view(request, path=''):
    """
    View temporária que será usada para todas as URLs marcadas com /temp/
    Mostra uma mensagem amigável informando que a página está em desenvolvimento
    """
    template = loader.get_template('accounts/temp_page.html')
    context = {
        'path': path,
        'title': path.replace('/', ' ').title().strip()
    }
    return HttpResponse(template.render(context, request))