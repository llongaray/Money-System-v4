from django.shortcuts import render

def welcome(request):
    return render(request, 'apps/dashboard/welcome.html')
