#coding: utf-8
from userdict_app.models import AlphabetLetters
from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from userdict_app.decode_unicode_references import decode_unicode_references
import urllib2

class Command(BaseCommand):
    '''
    Функция заполняет таблицу AlphabetLetters c помощью парсинга сайта http://www.nihongo.aikidoka.ru/
    '''
    can_import_settings = True
    def handle(self, *args, **options):
        for link in (('HR','http://www.nihongo.aikidoka.ru/59-propisi_hiragana.html'),('KT','http://www.nihongo.aikidoka.ru/60-propisi_katakana.html')):
            html_page = urllib2.urlopen(link[1]).read().decode('cp1251')
            soup_page = BeautifulSoup(html_page)
            katakana = soup_page.findAll(attrs={'lang':'JA'})
            for letter in katakana:
                reading = letter.parent.contents[2]
                if letter.a == None:
                    hieroglyph = decode_unicode_references(letter.text)
                else:
                    hieroglyph = decode_unicode_references(letter.a.text)
                print u"%s - %s (%s)"%(hieroglyph, reading, link[0])
                AlphabetLetters.objects.create(letter_type=link[0], letter = hieroglyph, pronunciation=reading)

