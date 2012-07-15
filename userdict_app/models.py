#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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

    hieroglyph = models.CharField(u'Иероглиф', max_length = 1, unique=True)
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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    kanji_list = models.ManyToManyField(Hieroglyphs, verbose_name=u'Словарь пользователя',
                                        through = 'userdict_app.HieroglyphUserInfo', blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'
        
    def __unicode__(self):
        return u'Профиль пользователя %s'%(self.user.username)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class HieroglyphUserInfo(models.Model):

    FAIL_CHOISES = (('KT','Kanji-Translation'),
                    ('TK','Translation-Kanji'),
                   )
    
    profile = models.ForeignKey(UserProfile, verbose_name=u'Профиль')
    hieroglyph = models.ForeignKey(Hieroglyphs, verbose_name=u'Иероглиф')    
    correct_exp = models.IntegerField(u'Опыт, полученный за правильные попытки распознания иероглифа', default=0)
    incorrect_exp = models.IntegerField(u'Опыт, не полученный за не правильные попытки распознания иероглифа', default=0)
    added_timestamp = models.DateTimeField(u'Дата добавления', auto_now_add = True)
    failed_timestamp = models.DateTimeField(u'Дата последнего нераспознавания', null=True, blank=True)
    last_fail = models.CharField(u'Тренировка, на которой иероглиф не был распознан',
                                 max_length = 2, choices = FAIL_CHOISES, null=True, blank=True)

    class Meta:
        ordering = ('profile', 'hieroglyph',)
        verbose_name = u'Информация о иероглифе в словаре пользователя'
        verbose_name_plural = u'Информация о иероглифах в словаре пользователя'
        
    def __unicode__(self):
        return "%20s (%2s) [%10s]"%(self.profile.user.username, self.hieroglyph.hieroglyph, self.status())

    def status(self):
        u'Метод вычисляет степень знания пользователем данного иероглифа.'

        # Опыт, необходиный для достижения определенной степени знания.
        # Вынести в общие настройки
        familiar_info = ((0, 'DONT KNOW'),
                         (2, 'FAMILIAR'),
                         (5, 'RECOGNIZE'),
                         (10, 'KNOW')
                         )
        exp = correct_exp - incorrect_exp
        for lvl in familiar_info:
            if exp in xrange(lvl[0]):
                return lvl[1]
        return familiar_info[-1][1]
