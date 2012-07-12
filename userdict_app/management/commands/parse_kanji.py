#coding: utf-8
from userdict_app.models import AlphabetLetters, Hieroglyphs
from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from userdict_app.decode_unicode_references import decode_unicode_references
import urllib2
import re

class Command(BaseCommand):
    '''
    Комманда скачивает иероглифы с сайта kanjidb.ru 
    '''
    can_import_settings = True
    def handle(self, *args, **options):
        kanji_amount = 2016 #Количество иероглифов на сайте
        totally_added = 0
        for kanji_id in xrange(1, kanji_amount):
            url = 'http://kanjidb.ru/?p=kanji_show&kanji_id=%s'%kanji_id
            html_page = urllib2.urlopen(url).read().decode('utf-8')
            soup_page = BeautifulSoup(html_page)
            if not soup_page.findAll(text=re.compile(u'Кандзи с таким идентификатором не найден')):
                kanji_info = soup_page.findAll(attrs={'cellpadding':'3', 'cellspacing':'1'})[0]
                kanji_td = soup_page.findAll('table', attrs={'cellpadding':'3'})
                kanji_text = kanji_td[0].contents[1].contents[1].contents[1]
                kanji_text = kanji_text.findAll(text=True)
                kanji = kanji_text[1]
                translation_raw = kanji_text[2]
                pattern = re.compile(u".*«(.*)».*")
                translation = pattern.match(translation_raw).group(1)
                image_url = kanji_info.findAll('img',)
                if len(image_url)!= 0:
                    image_url = image_url[0]['src'].encode('utf-8')
                    image_url = ''.join(('kanjidb.ru',image_url[1:]))
                else:
                    image_url = ''
                key = ''.join(kanji_info.findAll(text=u"ключ")[0].parent.parent.parent.parent.findAll(text=True)).split('(')[1].split(')')[0].encode('utf-8') #optimize me!
                on_reading = '/'.join(kanji_info.findAll(text=u"он")[0].parent.parent.parent.parent.contents[3].contents[0].findAll(text=True)[:-1])
                kun_reading = '/'.join(kanji_info.findAll(text=u"кун")[0].parent.parent.parent.parent.contents[3].findAll(text=True))
                features_amount = int(kanji_info.findAll(text=u"черт")[0].parent.parent.parent.parent.contents[3].contents[0].contents[0])
                jlpt_level = int(kanji_info.findAll(text=u"уровень")[0].parent.parent.parent.parent.contents[3].findAll(text=True)[1][-2])
                new_kanji = Hieroglyphs.objects.create(
                    hieroglyph = kanji,
                    key=key,
                    meaning = translation,
                    on_reading = on_reading,
                    kun_reading = kun_reading,
                    main_features = features_amount,
                    jlpt_level = jlpt_level
                    )
                totally_added+=1
                print "%s   [%s]"%(new_kanji, kanji_id)
        print "Totally added %s hieroglyphs!"%totally_added
