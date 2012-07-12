# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def mainpage(request):
    return render(request, 'mainpage.html')
