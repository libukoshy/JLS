#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class AlphabetLetters(models.Model):
    u'Символы алфавита'
    
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
    u'Иероглифы'
    
    JLPT_LEVELS = (('0', u'не входит в программу'),
                   ('1', 'JLPT - ku 1'),
                   ('2', 'JLPT - ku 2'),
                   ('3', 'JLPT - ku 3'),                   
                   ('4', 'JLPT - ku 4'),
                   ('5', 'JLPT - ku 5'),
                   )

    hieroglyph = models.CharField(u'Иероглиф', max_length = 1, unique=True)
    key = models.ForeignKey('HieroglyphKey', verbose_name=u'Ключ')
    meaning = models.CharField(u'Значение', max_length = 50)
    readings = models.ManyToManyField('HieroglyphReading', verbose_name=u'Онные и кунные чтения')
    additional_features = models.PositiveSmallIntegerField(u'Количество дополнительных черт')
    jlpt_level = models.CharField(u'Уровень экзамена, в программу которого входит иероглиф', max_length=1, choices=JLPT_LEVELS, null=True, blank=True)
    spelling = models.ImageField(u'Написание', upload_to='/hierogliphs/pics/', null=True, blank=True)
    similar_hieroglyphs = models.ManyToManyField('self', verbose_name=u'Похожие иероглифы', symmetrical = False, null=True, blank=True)
    contains = models.ManyToManyField('self', verbose_name = u'Входящие в состав иероглифы', null=True, blank=True)

    class Meta:
        ordering = ('key', 'hieroglyph',)
        verbose_name = u'Иероглиф'
        verbose_name_plural = u'Иероглифы'
        
    def __unicode__(self):
        return "%2s (%20s)   [%2s]"%(self.hieroglyph, self.meaning, self.key.key)


class HieroglyphKey(models.Model):
    u'Ключи (базовые иероглифы)'

    key = models.CharField(u'Иероглиф', max_length = 1)
#    meaning = models.CharField(u'Значение', max_length = 50)
    features_amount = models.PositiveSmallIntegerField(u'Количество черт', null=True, blank=True)
    number = models.PositiveSmallIntegerField(u'Номер')
#    readings = models.ManyToManyField('HieroglyphReading', verbose_name=u'Онные и кунные чтения')
    
    class Meta:
        ordering = ('number',)
        verbose_name = u'Ключ'
        verbose_name_plural = u'Ключи'
        
    def __unicode__(self):
        return u"%2s [%3s]"%(self.key, self.number)
    

class HieroglyphReading(models.Model):
    u'Чтения иероглифов'

    READING_TYPE_CHOICES = (('O','On'), ('K','Kun'))
    
    reading_type = models.CharField(u'Тип чтения', max_length = 1, choices = READING_TYPE_CHOICES)
    reading = models.CharField(u'Произношение', max_length = 30)

    class Meta:
        ordering = ('reading',)
        verbose_name = u'Произношениее иероглифа'
        verbose_name_plural = u'Произношения иероглифов'
        
    def __unicode__(self):
        return '[%s]'%(self.reading)
    

class Words(models.Model):
    u'Слова'
    
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
    u'Профиль пользователя'

    MAX_LEVEL = 10
    # Таблица необходимого опыта для каждого уровня
    LEVELS_TABLE = {
        1: 50,
        2: 100,
        3: 200,
        4: 300,
        5: 500,
        6: 800,
        7: 1200,
        8: 1800,
        9: 2500,
        10: 3200
                   }
    
    user = models.OneToOneField(User)
    full_name = models.CharField(u'Полное имя', max_length = 50)
    known_kanjs_amount = models.PositiveSmallIntegerField(u'Количество известных иероглифов', default = 0)    #PositiveSmallIntegerField хватит??
    kanji_list = models.ManyToManyField(Hieroglyphs, verbose_name=u'Словарь пользователя',
                                        through = 'userdict_app.HieroglyphUserInfo', blank=True)
    current_level = models.PositiveSmallIntegerField(u'Текущий уровень опыта', default = 0)
    current_exp = models.PositiveSmallIntegerField(u'Значение опыта на текущем уровне', default = 0)    #PositiveSmallIntegerField хватит??
    
    class Meta:
        ordering = ('user',)
        verbose_name = u'Профиль пользователя'
        verbose_name_plural = u'Профили пользователей'
        
    def __unicode__(self):
        return u'Профиль пользователя %s'%(self.user.username)

    def add_experiense(self, exp_amount):
        if self.current_level < UserProfile.MAX_LEVEL:
            exp_to_levelup = UserProfile.LEVELS_TABLE[self.current_level + 1] - self.current_exp
            if exp_amount < exp_to_levelup:
                self.current_exp += exp_amount
            else:
                self.current_level += 1
                self.current_exp = exp_amount - exp_to_levelup


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class HieroglyphUserInfo(models.Model):
    u'Таблица связи иероглифов с профилем пользователя'

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
