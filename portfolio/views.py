from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("portfolio/index.html")
    context = {
        "what?": 'what',
    }
    return HttpResponse(template.render(context, request))