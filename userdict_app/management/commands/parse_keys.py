#coding: utf-8
from userdict_app.models import AlphabetLetters, Hieroglyphs, HieroglyphReading, HieroglyphKey
from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from userdict_app.decode_unicode_references import decode_unicode_references
import urllib2
import re

class Command(BaseCommand):
    '''
    Комманда скачивает ключи с сайта nihongo.aikidoka.ru
    '''
    can_import_settings = True
    def handle(self, *args, **options):
        url = 'http://www.nihongo.aikidoka.ru/kanji_key.html'
        html_page = urllib2.urlopen(url).read().decode('cp1251')
        soup_page = BeautifulSoup(html_page)
        key_amount = 0
        for key_block in soup_page.findAll(attrs={'class':'kanji_tab'}):
            key_amount += 1
            hieroglyph = decode_unicode_references(key_block.contents[0].find(text=True))
            number = key_block.contents[2].find(text=True)
            print hieroglyph, number
            HieroglyphKey.objects.create(key = hieroglyph, number = number)
        print "Считано %s ключей."%key_amount

