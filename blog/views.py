from django.shortcuts import render
from django.core.management import call_command

def archives(request):
    call_command("build")
    return render(request, "archive/index.html")

