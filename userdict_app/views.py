# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from models import AlphabetLetters, Hieroglyphs, Words
from django.core.paginator import Paginator

def mainpage(request):
    return render(request, 'mainpage.html')

def kanji_list(request, page):
    kanji_per_page = 24
    page = int(page)
    p = Paginator(Hieroglyphs.objects.all(), kanji_per_page)
    page = p.page(page)
    kanjis = page.object_list
    return render(request, 'userdict_app/kanji_list.html', {'kanjis':kanjis, 'page_obj':page})
