#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

class AlphabetLetters(models.Model):
    u'Символ алфавита'
    
    ALPHABET_CHOISES = (('HR','Hiragana'),('KT','Katakana'))

    letter_type = models.CharField(u'Тип символа',max_length=2, choices=ALPHABET_CHOISES)
    letter = models.CharField(u'Обозначение', max_length=2, unique=True)
    pronunciation = models.CharField(u'Произношение', max_length=10)
    spelling = models.ImageField(u'Написание', upload_to='/alphabet_pics/', null=True, blank=True)
    description = models.CharField(u'Короткая доп.информация', max_length=500, null=True, blank=True)

    class Meta:
        ordering = ('letter_type','letter')
        verbose_name = u'Символ алфавита'
        verbose_name_plural = u'Символы алфавита'
        
    def __unicode__(self):
        return self.letter

    
class Hieroglyphs(models.Model):

    JLPT_LEVELS = (('0', u'не входит в программу'),
                   ('1', 'JLPT - ku 1'),
                   ('2', 'JLPT - ku 2'),
                   ('3', 'JLPT - ku 3'),                   
                   ('4', 'JLPT - ku 4'),
                   ('5', 'JLPT - ku 5'),
                   )

    hieroglyph = models.CharField(u'Иероглиф', max_length = 1)
    key = models.CharField(u'Ключ', max_length=10) 
    meaning = models.CharField(u'Значение', max_length = 50)
    on_reading = models.CharField(u'Онное чтение', max_length=20, null=True, blank=True)
    kun_reading = models.CharField(u'Кунное чтение', max_length=20, null=True, blank=True)
    main_features = models.IntegerField(u'Количество главных черт')
    jlpt_level = models.CharField(u'Уровень экзамена, в программу которого входит иероглиф', max_length=1, choices=JLPT_LEVELS, null=True, blank=True)
    spelling = models.ImageField(u'Написание', upload_to='/hierogliphs/pics/', null=True, blank=True)
    similar_hieroglyphs = models.ManyToManyField('self', verbose_name=u'Похожие иероглифы', symmetrical = False, null=True, blank=True)
    contains = models.ManyToManyField('self', verbose_name = u'Входящие в состав иероглифы', null=True, blank=True)

    class Meta:
        ordering = ('key', 'hieroglyph',)
        verbose_name = u'Иероглиф'
        verbose_name_plural = u'Иероглифы'
        
    def __unicode__(self):
        return "%2s (%20s)   [%7s]"%(self.hieroglyph, self.meaning, self.key)
    

class Words(models.Model):
    word = models.CharField(u'Слово на японском', max_length = 20)
    translation = models.CharField(u'Перевод', max_length = 100)
    reading = models.CharField(u'Произношение', max_length = 40)

    class Meta:
        ordering = ('word',)
        verbose_name = u'Слово'
        verbose_name_plural = u'Слова'
        
    def __unicode__(self):
        return "%s [%s] %s"%(self.word, self.reading, self.translation)
