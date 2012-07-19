#coding: utf-8
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from models import AlphabetLetters, Hieroglyphs, Words, HieroglyphUserInfo
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

def mainpage(request):
    return render(request, 'mainpage.html')

def kanji_list(request, page):
    kanji_per_page = 24
    page = int(page)
    p = Paginator(Hieroglyphs.objects.all(), kanji_per_page)
    # TODO проверять количество страниц
    page = p.page(page)
    kanjis = page.object_list
    return render(request, 'userdict_app/kanji_list.html', {'kanjis':kanjis, 'page_obj':page})

@login_required
def profile_page(request):
    # Количество показываемых "недавних" иероглифов
    # Вынести в настройки
    recently_kanji_size = 50
    
    kanji = Hieroglyphs.objects.all()
    recently_added = request.user.get_profile().kanji_list.order_by('-hieroglyphuserinfo__added_timestamp')[:recently_kanji_size]
    recently_failed = request.user.get_profile().kanji_list.filter(hieroglyphuserinfo__failed_timestamp__isnull=False).order_by('-hieroglyphuserinfo__failed_timestamp')[:recently_kanji_size]
    user_dict = request.user.get_profile().kanji_list.all()
    return render(request, 'userdict_app/profile_page.html', {'dict':user_dict, 'added':recently_added, 'failed':recently_failed})

@login_required
@require_POST
def add_kanji_to_userdict(request):
    if 'kanji' in request.POST:
        HieroglyphUserInfo.objects.create(profile=request.user.get_profile(),
                                          hieroglyph = Hieroglyphs.objects.get(hieroglyph=request.POST['kanji'])).save()
        messages.success(request, u'Иероглиф добавлен в словарь.')
        return redirect(request.POST.get('next', reverse('kanji_list', args=[1,])))
    else:
        raise Http404                                          

@login_required
@require_POST
def remove_kanji_from_userdict(request):
    if 'kanji' in request.POST:
        HieroglyphUserInfo.objects.filter(profile=request.user.get_profile(),
                                          hieroglyph = Hieroglyphs.objects.get(hieroglyph=request.POST['kanji'])).delete()
        messages.success(request, u'Иероглиф удален.')
        return redirect(request.POST.get('next', reverse('kanji_list', args=[1,])))
    else:
        raise Http404                                          

def kanji_info(request, kanji):
    kanji = get_object_or_404(Hieroglyphs, hieroglyph = kanji)
    on_readings = kanji.readings.filter(reading_type = 'O')
    kun_readings = kanji.readings.filter(reading_type = 'K')
    print on_readings
    print kun_readings
    return render(request, 'userdict_app/kanji_info.html', {'kanji':kanji, 'on_readings':on_readings, 'kun_readings':kun_readings})
