from django.shortcuts import redirect
from django.views import View


def redirect_view(request):
    return redirect('/news/')
