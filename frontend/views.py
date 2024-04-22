from django.shortcuts import render


def auth(request):
    return render(request, "index.html")


def check_code(request):
    return render(request, "code.html")


def user(request):
    return render(request, "user.html")


def link_user(request):
    return render(request, "link_user.html")