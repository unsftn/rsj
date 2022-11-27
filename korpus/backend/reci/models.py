# -*- coding: utf-8 -*-
import itertools
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

OPERACIJE_IZMENE = [
    (1, 'креирана реч'),
    (2, 'измењена реч'),
]

VRSTE_RECI = {
    0: 'именица',
    1: 'глагол',
    2: 'придев',
    3: 'прилог',
    4: 'предлог',
    5: 'заменица',
    6: 'узвик',
    7: 'речца',
    8: 'везник',
    9: 'број',
    10: 'остало',
}

VRSTE_IMENICA = [
    (1, 'апстрактна'),
    (2, 'заједничка'),
    (3, 'властита'),
    (4, 'збирна'),
    (5, 'градивна'),
    (6, 'глаголска'),
]

GLAGOLSKI_VID = [
    (1, 'свршени'),
    (2, 'несвршени'),
    (3, 'свршени и несвршени'),
    (4, 'несвршени и свршени'),
    (5, 'свршени (несвршени)'),
    (6, 'несвршени (свршени)'),
]

GLAGOLSKI_ROD = [
    (1, 'прелазни'),
    (2, 'непрелазни'),
    (3, 'повратни'),
    (4, 'прелазни и непрелазни'),
    (5, 'непрелазни и прелазни'),
    (6, 'прелазни (непрелазни)'),
    (7, 'непрелазни (прелазни)'),
]

GLAGOLSKO_VREME = [
    (1, 'презент'),
    (2, 'футур 1'),
    (3, 'аорист'),
    (4, 'имперфекат'),
    (5, 'императив'),
]

OBLIK_GLAGOLSKE_VARIJANTE = [
    (1, 'пр.л.јед.'),
    (2, 'др.л.јед.'),
    (3, 'тр.л.јед.'),
    (4, 'пр.л.мн.'),
    (5, 'др.л.мн.'),
    (6, 'тр.л.мн.'),
]

PRIDEVSKI_VID = [
    (1, 'одређени'),
    (2, 'неодређени'),
    (3, 'компаратив'),
    (4, 'суперлатив'),
]

ROD = [
    (1, 'мушки'),
    (2, 'женски'),
    (3, 'средњи'),
]

def svi_atributi_prideva():
    rodovi_stepeni = ['mo', 'mn', 'mk', 'ms', 'zp', 'zk', 'zs', 'sp', 'sk', 'ss']
    padezi = ['nom', 'gen', 'dat', 'aku', 'vok', 'ins', 'lok']
    brojevi = ['jed', 'mno']
    kombinacije = itertools.product(rodovi_stepeni, padezi, brojevi)
    atributi = [k[0]+k[1]+k[2] for k in kombinacije]
    return atributi


def svi_atributi_varijante_prideva():
    stepeni = ['o', 'n', 'p', 'k', 's']
    padezi = ['nom', 'gen', 'dat', 'aku', 'vok', 'ins', 'lok']
    brojevi = ['jed']
    kombinacije = itertools.product(stepeni, padezi, brojevi)
    atributi = [k[0]+k[1]+k[2] for k in kombinacije]
    return atributi


ATRIBUTI_PRIDEVA = svi_atributi_prideva()

ATRIBUTI_VARIJANTE_PRIDEVA = svi_atributi_varijante_prideva()


def _append_attr(array, obj, attr_name):
    """
    Dodaje na kraj niza array vrednost atributa pod nazivom attr_name objekta obj, ako atribut i vrednost postoje
    """
    if hasattr(obj, attr_name):
        value = getattr(obj, attr_name)
        if value:
            array.append(value)


class UserProxy(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.email + ')'

    def puno_ime(self):
        return self.first_name + ' ' + self.last_name


class StatusReci(models.Model):
    naziv = models.CharField('назив', max_length=50)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name = 'статус речи'
        verbose_name_plural = 'статуси речи'
        ordering = ['id']


class Imenica(models.Model):
    nomjed = models.CharField('номинатив једнине', max_length=50)
    genjed = models.CharField('генитив једнине', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив једнине', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив једнине', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив једнине', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал једнине', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив једнине', max_length=50, blank=True, null=True)
    nommno = models.CharField('номинатив множине', max_length=50, blank=True, null=True)
    genmno = models.CharField('генитив множине', max_length=50, blank=True, null=True)
    datmno = models.CharField('датив множине', max_length=50, blank=True, null=True)
    akumno = models.CharField('акузатив множине', max_length=50, blank=True, null=True)
    vokmno = models.CharField('вокатив множине', max_length=50, blank=True, null=True)
    insmno = models.CharField('инструментал множине', max_length=50, blank=True, null=True)
    lokmno = models.CharField('локатив множине', max_length=50, blank=True, null=True)
    vrsta = models.IntegerField('врста именице', choices=VRSTE_IMENICA, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'именица'
        verbose_name_plural = 'именице'
        ordering = ['id']
        indexes = [
            models.Index(fields=['vrsta']),
            models.Index(fields=['nomjed'])
        ]

    def __str__(self):
        return f'{self.id}: {self.nomjed}'

    def osnovni_oblik(self) -> str:
        return self.nomjed

    def vrsta_reci(self) -> int:
        return 0

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[0]

    def oblici(self) -> list:
        retval = _svi_oblici_imenice(self)
        for var in self.varijantaimenice_set.all():
            retval.extend(_svi_oblici_imenice(var))
        return retval


class VarijantaImenice(models.Model):
    imenica = models.ForeignKey(Imenica, verbose_name='именица', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    nomjed = models.CharField('номинатив једнине', max_length=50, blank=True, null=True)
    genjed = models.CharField('генитив једнине', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив једнине', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив једнине', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив једнине', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал једнине', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив једнине', max_length=50, blank=True, null=True)
    nommno = models.CharField('номинатив множине', max_length=50, blank=True, null=True)
    genmno = models.CharField('генитив множине', max_length=50, blank=True, null=True)
    datmno = models.CharField('датив множине', max_length=50, blank=True, null=True)
    akumno = models.CharField('акузатив множине', max_length=50, blank=True, null=True)
    vokmno = models.CharField('вокатив множине', max_length=50, blank=True, null=True)
    insmno = models.CharField('инструментал множине', max_length=50, blank=True, null=True)
    lokmno = models.CharField('локатив множине', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'варијанта именице'
        verbose_name_plural = 'варијанте именица'


class IzmenaImenice(models.Model):
    imenica = models.ForeignKey(Imenica, verbose_name='именица', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена именице'
        verbose_name_plural = 'измене именица'


def _svi_oblici_imenice(imenica):
    retval = []
    for x in ['nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed', 'nommno', 'genmno', 'datmno',
              'akumno', 'vokmno', 'insmno', 'lokmno']:
        _append_attr(retval, imenica, x)
    return retval


class Glagol(models.Model):
    gl_rod = models.IntegerField('глаголски род', choices=GLAGOLSKI_ROD, blank=True, null=True)
    gl_vid = models.IntegerField('глаголски вид', choices=GLAGOLSKI_VID, blank=True, null=True)
    infinitiv = models.CharField('инфинитив', max_length=50, blank=True, null=True)
    rgp_mj = models.CharField('ргп м.јед.', max_length=50, blank=True, null=True)
    rgp_zj = models.CharField('ргп ж.јед.', max_length=50, blank=True, null=True)
    rgp_sj = models.CharField('ргп с.јед.', max_length=50, blank=True, null=True)
    rgp_mm = models.CharField('ргп м.мн.', max_length=50, blank=True, null=True)
    rgp_zm = models.CharField('ргп ж.мн.', max_length=50, blank=True, null=True)
    rgp_sm = models.CharField('ргп с.мн.', max_length=50, blank=True, null=True)
    tgp_mj = models.CharField('тгп м.јед.', max_length=50, blank=True, null=True)
    tgp_zj = models.CharField('тгп ж.јед.', max_length=50, blank=True, null=True)
    tgp_sj = models.CharField('тгп с.јед.', max_length=50, blank=True, null=True)
    tgp_mm = models.CharField('тгп м.мн.', max_length=50, blank=True, null=True)
    tgp_zm = models.CharField('тгп ж.мн.', max_length=50, blank=True, null=True)
    tgp_sm = models.CharField('тгп с.мн.', max_length=50, blank=True, null=True)
    gpp = models.CharField('гл.прил. прошли', max_length=50, blank=True, null=True)
    gps = models.CharField('гл.прил. садашњи', max_length=50, blank=True, null=True)
    gpp2 = models.CharField('гл.прил. садашњи, варијанта', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'глагол'
        verbose_name_plural = 'глаголи'
        ordering = ['id']
        indexes = [
            models.Index(fields=['infinitiv']),
        ]

    def __str__(self):
        return f'{self.id}: {self.infinitiv}'

    def osnovni_oblik(self) -> str:
        return self.infinitiv

    def vrsta_reci(self) -> int:
        return 1

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[1]

    def oblici(self) -> list:
        retval = [self.infinitiv]
        retval.extend(_svi_oblici_glagola(self))
        return retval


class OblikGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    vreme = models.IntegerField('време', choices=GLAGOLSKO_VREME)
    jd1 = models.CharField('прво лице једнине', max_length=50, blank=True, null=True)
    jd2 = models.CharField('друго лице једнине', max_length=50, blank=True, null=True)
    jd3 = models.CharField('треће лице једнине', max_length=50, blank=True, null=True)
    mn1 = models.CharField('прво лице множине', max_length=50, blank=True, null=True)
    mn2 = models.CharField('друго лице множине', max_length=50, blank=True, null=True)
    mn3 = models.CharField('треће лице множине', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'глаголски облик'
        verbose_name_plural = 'глаголски облици'
        ordering = ['vreme']
        indexes = [
            models.Index(fields=['jd1']),
            models.Index(fields=['glagol', 'vreme'])
        ]

    def __str__(self):
        return f'{self.glagol.id}: {self.vreme}: {self.jd1}'


class VarijanteGlagola(models.Model):
    oblik_glagola = models.ForeignKey(OblikGlagola, verbose_name='облик глагола', on_delete=models.CASCADE)
    varijanta = models.IntegerField('варијанта', choices=OBLIK_GLAGOLSKE_VARIJANTE)
    tekst = models.CharField('текст', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'варијанта глагола'
        verbose_name_plural = 'варијанте глагола'
        ordering = ['id']

    def __str__(self):
        return f'{self.oblik_glagola.glagol.id}: {self.oblik_glagola.vreme}: {self.tekst}'


class IzmenaGlagola(models.Model):
    glagol = models.ForeignKey(Glagol, verbose_name='глагол', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена глагола'
        verbose_name_plural = 'измене глагола'


def _svi_oblici_glagola(glagol):
    retval = []
    for oblik in glagol.oblikglagola_set.all():
        for x in ['jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3']:
            _append_attr(retval, oblik, x)
        for var in oblik.varijanteglagola_set.all():
            _append_attr(retval, var, 'tekst')
    return retval


class Pridev(models.Model):
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    lema = models.CharField('лема', max_length=50, blank=True, null=True)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)
    dva_vida = models.BooleanField('два вида', default=True)

    monomjed = models.TextField('мушки одређени номинатив једнина', blank=True, null=True)
    mogenjed = models.TextField('мушки одређени генитив једнина', blank=True, null=True)
    modatjed = models.TextField('мушки одређени датив једнина', blank=True, null=True)
    moakujed = models.TextField('мушки одређени акузатив једнина', blank=True, null=True)
    movokjed = models.TextField('мушки одређени вокатив једнина', blank=True, null=True)
    moinsjed = models.TextField('мушки одређени инструментал једнина', blank=True, null=True)
    molokjed = models.TextField('мушки одређени локатив једнина', blank=True, null=True)
    monommno = models.TextField('мушки одређени номинатив множина', blank=True, null=True)
    mogenmno = models.TextField('мушки одређени генитив множина', blank=True, null=True)
    modatmno = models.TextField('мушки одређени датив множина', blank=True, null=True)
    moakumno = models.TextField('мушки одређени акузатив множина', blank=True, null=True)
    movokmno = models.TextField('мушки одређени вокатив множина', blank=True, null=True)
    moinsmno = models.TextField('мушки одређени инструментал множина', blank=True, null=True)
    molokmno = models.TextField('мушки одређени локатив множина', blank=True, null=True)

    mnnomjed = models.TextField('мушки неодређени номинатив једнина', blank=True, null=True)
    mngenjed = models.TextField('мушки неодређени генитив једнина', blank=True, null=True)
    mndatjed = models.TextField('мушки неодређени датив једнина', blank=True, null=True)
    mnakujed = models.TextField('мушки неодређени акузатив једнина', blank=True, null=True)
    mnvokjed = models.TextField('мушки неодређени вокатив једнина', blank=True, null=True)
    mninsjed = models.TextField('мушки неодређени инструментал једнина', blank=True, null=True)
    mnlokjed = models.TextField('мушки неодређени локатив једнина', blank=True, null=True)
    mnnommno = models.TextField('мушки неодређени номинатив множина', blank=True, null=True)
    mngenmno = models.TextField('мушки неодређени генитив множина', blank=True, null=True)
    mndatmno = models.TextField('мушки неодређени датив множина', blank=True, null=True)
    mnakumno = models.TextField('мушки неодређени акузатив множина', blank=True, null=True)
    mnvokmno = models.TextField('мушки неодређени вокатив множина', blank=True, null=True)
    mninsmno = models.TextField('мушки неодређени инструментал множина', blank=True, null=True)
    mnlokmno = models.TextField('мушки неодређени локатив множина', blank=True, null=True)

    mknomjed = models.TextField('мушки компаратив номинатив једнина', blank=True, null=True)
    mkgenjed = models.TextField('мушки компаратив генитив једнина', blank=True, null=True)
    mkdatjed = models.TextField('мушки компаратив датив једнина', blank=True, null=True)
    mkakujed = models.TextField('мушки компаратив акузатив једнина', blank=True, null=True)
    mkvokjed = models.TextField('мушки компаратив вокатив једнина', blank=True, null=True)
    mkinsjed = models.TextField('мушки компаратив инструментал једнина', blank=True, null=True)
    mklokjed = models.TextField('мушки компаратив локатив једнина', blank=True, null=True)
    mknommno = models.TextField('мушки компаратив номинатив множина', blank=True, null=True)
    mkgenmno = models.TextField('мушки компаратив генитив множина', blank=True, null=True)
    mkdatmno = models.TextField('мушки компаратив датив множина', blank=True, null=True)
    mkakumno = models.TextField('мушки компаратив акузатив множина', blank=True, null=True)
    mkvokmno = models.TextField('мушки компаратив вокатив множина', blank=True, null=True)
    mkinsmno = models.TextField('мушки компаратив инструментал множина', blank=True, null=True)
    mklokmno = models.TextField('мушки компаратив локатив множина', blank=True, null=True)
    
    msnomjed = models.TextField('мушки суперлатив номинатив једнина', blank=True, null=True)
    msgenjed = models.TextField('мушки суперлатив генитив једнина', blank=True, null=True)
    msdatjed = models.TextField('мушки суперлатив датив једнина', blank=True, null=True)
    msakujed = models.TextField('мушки суперлатив акузатив једнина', blank=True, null=True)
    msvokjed = models.TextField('мушки суперлатив вокатив једнина', blank=True, null=True)
    msinsjed = models.TextField('мушки суперлатив инструментал једнина', blank=True, null=True)
    mslokjed = models.TextField('мушки суперлатив локатив једнина', blank=True, null=True)
    msnommno = models.TextField('мушки суперлатив номинатив множина', blank=True, null=True)
    msgenmno = models.TextField('мушки суперлатив генитив множина', blank=True, null=True)
    msdatmno = models.TextField('мушки суперлатив датив множина', blank=True, null=True)
    msakumno = models.TextField('мушки суперлатив акузатив множина', blank=True, null=True)
    msvokmno = models.TextField('мушки суперлатив вокатив множина', blank=True, null=True)
    msinsmno = models.TextField('мушки суперлатив инструментал множина', blank=True, null=True)
    mslokmno = models.TextField('мушки суперлатив локатив множина', blank=True, null=True)

    zpnomjed = models.TextField('женски позитив номинатив једнина', blank=True, null=True)
    zpgenjed = models.TextField('женски позитив генитив једнина', blank=True, null=True)
    zpdatjed = models.TextField('женски позитив датив једнина', blank=True, null=True)
    zpakujed = models.TextField('женски позитив акузатив једнина', blank=True, null=True)
    zpvokjed = models.TextField('женски позитив вокатив једнина', blank=True, null=True)
    zpinsjed = models.TextField('женски позитив инструментал једнина', blank=True, null=True)
    zplokjed = models.TextField('женски позитив локатив једнина', blank=True, null=True)
    zpnommno = models.TextField('женски позитив номинатив множина', blank=True, null=True)
    zpgenmno = models.TextField('женски позитив генитив множина', blank=True, null=True)
    zpdatmno = models.TextField('женски позитив датив множина', blank=True, null=True)
    zpakumno = models.TextField('женски позитив акузатив множина', blank=True, null=True)
    zpvokmno = models.TextField('женски позитив вокатив множина', blank=True, null=True)
    zpinsmno = models.TextField('женски позитив инструментал множина', blank=True, null=True)
    zplokmno = models.TextField('женски позитив локатив множина', blank=True, null=True)

    zknomjed = models.TextField('женски компаратив номинатив једнина', blank=True, null=True)
    zkgenjed = models.TextField('женски компаратив генитив једнина', blank=True, null=True)
    zkdatjed = models.TextField('женски компаратив датив једнина', blank=True, null=True)
    zkakujed = models.TextField('женски компаратив акузатив једнина', blank=True, null=True)
    zkvokjed = models.TextField('женски компаратив вокатив једнина', blank=True, null=True)
    zkinsjed = models.TextField('женски компаратив инструментал једнина', blank=True, null=True)
    zklokjed = models.TextField('женски компаратив локатив једнина', blank=True, null=True)
    zknommno = models.TextField('женски компаратив номинатив множина', blank=True, null=True)
    zkgenmno = models.TextField('женски компаратив генитив множина', blank=True, null=True)
    zkdatmno = models.TextField('женски компаратив датив множина', blank=True, null=True)
    zkakumno = models.TextField('женски компаратив акузатив множина', blank=True, null=True)
    zkvokmno = models.TextField('женски компаратив вокатив множина', blank=True, null=True)
    zkinsmno = models.TextField('женски компаратив инструментал множина', blank=True, null=True)
    zklokmno = models.TextField('женски компаратив локатив множина', blank=True, null=True)
    
    zsnomjed = models.TextField('женски суперлатив номинатив једнина', blank=True, null=True)
    zsgenjed = models.TextField('женски суперлатив генитив једнина', blank=True, null=True)
    zsdatjed = models.TextField('женски суперлатив датив једнина', blank=True, null=True)
    zsakujed = models.TextField('женски суперлатив акузатив једнина', blank=True, null=True)
    zsvokjed = models.TextField('женски суперлатив вокатив једнина', blank=True, null=True)
    zsinsjed = models.TextField('женски суперлатив инструментал једнина', blank=True, null=True)
    zslokjed = models.TextField('женски суперлатив локатив једнина', blank=True, null=True)
    zsnommno = models.TextField('женски суперлатив номинатив множина', blank=True, null=True)
    zsgenmno = models.TextField('женски суперлатив генитив множина', blank=True, null=True)
    zsdatmno = models.TextField('женски суперлатив датив множина', blank=True, null=True)
    zsakumno = models.TextField('женски суперлатив акузатив множина', blank=True, null=True)
    zsvokmno = models.TextField('женски суперлатив вокатив множина', blank=True, null=True)
    zsinsmno = models.TextField('женски суперлатив инструментал множина', blank=True, null=True)
    zslokmno = models.TextField('женски суперлатив локатив множина', blank=True, null=True)

    spnomjed = models.TextField('средњи позитив номинатив једнина', blank=True, null=True)
    spgenjed = models.TextField('средњи позитив генитив једнина', blank=True, null=True)
    spdatjed = models.TextField('средњи позитив датив једнина', blank=True, null=True)
    spakujed = models.TextField('средњи позитив акузатив једнина', blank=True, null=True)
    spvokjed = models.TextField('средњи позитив вокатив једнина', blank=True, null=True)
    spinsjed = models.TextField('средњи позитив инструментал једнина', blank=True, null=True)
    splokjed = models.TextField('средњи позитив локатив једнина', blank=True, null=True)
    spnommno = models.TextField('средњи позитив номинатив множина', blank=True, null=True)
    spgenmno = models.TextField('средњи позитив генитив множина', blank=True, null=True)
    spdatmno = models.TextField('средњи позитив датив множина', blank=True, null=True)
    spakumno = models.TextField('средњи позитив акузатив множина', blank=True, null=True)
    spvokmno = models.TextField('средњи позитив вокатив множина', blank=True, null=True)
    spinsmno = models.TextField('средњи позитив инструментал множина', blank=True, null=True)
    splokmno = models.TextField('средњи позитив локатив множина', blank=True, null=True)

    sknomjed = models.TextField('средњи компаратив номинатив једнина', blank=True, null=True)
    skgenjed = models.TextField('средњи компаратив генитив једнина', blank=True, null=True)
    skdatjed = models.TextField('средњи компаратив датив једнина', blank=True, null=True)
    skakujed = models.TextField('средњи компаратив акузатив једнина', blank=True, null=True)
    skvokjed = models.TextField('средњи компаратив вокатив једнина', blank=True, null=True)
    skinsjed = models.TextField('средњи компаратив инструментал једнина', blank=True, null=True)
    sklokjed = models.TextField('средњи компаратив локатив једнина', blank=True, null=True)
    sknommno = models.TextField('средњи компаратив номинатив множина', blank=True, null=True)
    skgenmno = models.TextField('средњи компаратив генитив множина', blank=True, null=True)
    skdatmno = models.TextField('средњи компаратив датив множина', blank=True, null=True)
    skakumno = models.TextField('средњи компаратив акузатив множина', blank=True, null=True)
    skvokmno = models.TextField('средњи компаратив вокатив множина', blank=True, null=True)
    skinsmno = models.TextField('средњи компаратив инструментал множина', blank=True, null=True)
    sklokmno = models.TextField('средњи компаратив локатив множина', blank=True, null=True)
    
    ssnomjed = models.TextField('средњи суперлатив номинатив једнина', blank=True, null=True)
    ssgenjed = models.TextField('средњи суперлатив генитив једнина', blank=True, null=True)
    ssdatjed = models.TextField('средњи суперлатив датив једнина', blank=True, null=True)
    ssakujed = models.TextField('средњи суперлатив акузатив једнина', blank=True, null=True)
    ssvokjed = models.TextField('средњи суперлатив вокатив једнина', blank=True, null=True)
    ssinsjed = models.TextField('средњи суперлатив инструментал једнина', blank=True, null=True)
    sslokjed = models.TextField('средњи суперлатив локатив једнина', blank=True, null=True)
    ssnommno = models.TextField('средњи суперлатив номинатив множина', blank=True, null=True)
    ssgenmno = models.TextField('средњи суперлатив генитив множина', blank=True, null=True)
    ssdatmno = models.TextField('средњи суперлатив датив множина', blank=True, null=True)
    ssakumno = models.TextField('средњи суперлатив акузатив множина', blank=True, null=True)
    ssvokmno = models.TextField('средњи суперлатив вокатив множина', blank=True, null=True)
    ssinsmno = models.TextField('средњи суперлатив инструментал множина', blank=True, null=True)
    sslokmno = models.TextField('средњи суперлатив локатив множина', blank=True, null=True)

    class Meta:
        verbose_name = 'придев'
        verbose_name_plural = 'придеви'
        ordering = ['id']
        indexes = [
            models.Index(fields=['lema'])
        ]

    def __str__(self):
        return f'{self.id}: {self.lema}'

    def osnovni_oblik(self) -> str:
        return self.lema if self.lema else self.prvi_popunjen_oblik()

    def vrsta_reci(self) -> int:
        return 2

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[2]

    def oblici(self) -> list:
        return _svi_oblici_prideva(self)

    def prvi_popunjen_oblik(self) -> str:
        for attr in ['monomjed', 'monommno', 'mnnomjed', 'mnnommno', 'mknomjed', 'mknommno', 'msnomjed',
                     'msnommno', 'zpnomjed', 'zpnommno', 'zknomjed', 'zknommno', 'zsnomjed', 'zsnommno',
                     'spnomjed', 'spnommno', 'sknomjed', 'sknommno', 'ssnomjed', 'ssnommno']:
            value = getattr(self, attr)
            if value:
                return value
        return ''


class VarijantaPrideva(models.Model):
    pridev = models.ForeignKey(Pridev, verbose_name='придев', on_delete=models.CASCADE)
    rod = models.IntegerField('род', choices=ROD)
    redni_broj = models.IntegerField('редни број')
    onomjed = models.TextField('одређени номинатив једнина', blank=True, null=True)
    ogenjed = models.TextField('одређени генитив једнина', blank=True, null=True)
    odatjed = models.TextField('одређени датив једнина', blank=True, null=True)
    oakujed = models.TextField('одређени акузатив једнина', blank=True, null=True)
    ovokjed = models.TextField('одређени вокатив једнина', blank=True, null=True)
    oinsjed = models.TextField('одређени инструментал једнина', blank=True, null=True)
    olokjed = models.TextField('одређени локатив једнина', blank=True, null=True)
    nnomjed = models.TextField('неодређени номинатив једнина', blank=True, null=True)
    ngenjed = models.TextField('неодређени генитив једнина', blank=True, null=True)
    ndatjed = models.TextField('неодређени датив једнина', blank=True, null=True)
    nakujed = models.TextField('неодређени акузатив једнина', blank=True, null=True)
    nvokjed = models.TextField('неодређени вокатив једнина', blank=True, null=True)
    ninsjed = models.TextField('неодређени инструментал једнина', blank=True, null=True)
    nlokjed = models.TextField('неодређени локатив једнина', blank=True, null=True)
    pnomjed = models.TextField('позитив номинатив једнина', blank=True, null=True)
    pgenjed = models.TextField('позитив генитив једнина', blank=True, null=True)
    pdatjed = models.TextField('позитив датив једнина', blank=True, null=True)
    pakujed = models.TextField('позитив акузатив једнина', blank=True, null=True)
    pvokjed = models.TextField('позитив вокатив једнина', blank=True, null=True)
    pinsjed = models.TextField('позитив инструментал једнина', blank=True, null=True)
    plokjed = models.TextField('позитив локатив једнина', blank=True, null=True)
    knomjed = models.TextField('компаратив номинатив једнина', blank=True, null=True)
    kgenjed = models.TextField('компаратив генитив једнина', blank=True, null=True)
    kdatjed = models.TextField('компаратив датив једнина', blank=True, null=True)
    kakujed = models.TextField('компаратив акузатив једнина', blank=True, null=True)
    kvokjed = models.TextField('компаратив вокатив једнина', blank=True, null=True)
    kinsjed = models.TextField('компаратив инструментал једнина', blank=True, null=True)
    klokjed = models.TextField('компаратив локатив једнина', blank=True, null=True)
    snomjed = models.TextField('суперлатив номинатив једнина', blank=True, null=True)
    sgenjed = models.TextField('суперлатив генитив једнина', blank=True, null=True)
    sdatjed = models.TextField('суперлатив датив једнина', blank=True, null=True)
    sakujed = models.TextField('суперлатив акузатив једнина', blank=True, null=True)
    svokjed = models.TextField('суперлатив вокатив једнина', blank=True, null=True)
    sinsjed = models.TextField('суперлатив инструментал једнина', blank=True, null=True)
    slokjed = models.TextField('суперлатив локатив једнина', blank=True, null=True)

    class Meta:
        verbose_name = 'варијанта придева'
        verbose_name_plural = 'варијанте придева'
        ordering = ['redni_broj']

    def __str__(self):
        return f'{self.id}'


class IzmenaPrideva(models.Model):
    pridev = models.ForeignKey(Pridev, verbose_name='придев', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена придева'
        verbose_name_plural = 'измене придева'


def _svi_oblici_prideva(pridev):
    retval = [pridev.lema]
    for attr in ATRIBUTI_PRIDEVA:
        _append_attr(retval, pridev, attr)
    for vp in pridev.varijantaprideva_set.all():
        for attr in ATRIBUTI_VARIJANTE_PRIDEVA:
            _append_attr(retval, vp, attr)
    return retval


class Predlog(models.Model):
    tekst = models.CharField(max_length=100)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'предлог'
        verbose_name_plural = 'предлози'

    def oblici(self) -> list:
        return [self.tekst]

    def osnovni_oblik(self) -> str:
        return self.tekst

    def vrsta_reci(self) -> int:
        return 4

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[4]

    def __str__(self):
        return f'{self.id}: {self.tekst}'


class IzmenaPredloga(models.Model):
    predlog = models.ForeignKey(Predlog, verbose_name='предлог', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена предлога'
        verbose_name_plural = 'измене предлога'


class Uzvik(models.Model):
    tekst = models.CharField(max_length=100)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'узвик'
        verbose_name_plural = 'узвици'

    def oblici(self) -> list:
        return [self.tekst]

    def osnovni_oblik(self) -> str:
        return self.tekst

    def vrsta_reci(self) -> int:
        return 6

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[6]

    def __str__(self):
        return f'{self.id}: {self.tekst}'


class IzmenaUzvika(models.Model):
    uzvik = models.ForeignKey(Uzvik, verbose_name='узвик', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена узвика'
        verbose_name_plural = 'измене узвика'


class Recca(models.Model):
    tekst = models.CharField(max_length=100)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'речца'
        verbose_name_plural = 'речце'

    def oblici(self) -> list:
        return [self.tekst]

    def osnovni_oblik(self) -> str:
        return self.tekst

    def vrsta_reci(self) -> int:
        return 7

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[7]

    def __str__(self):
        return f'{self.id}: {self.tekst}'


class IzmenaRecce(models.Model):
    recca = models.ForeignKey(Recca, verbose_name='речца', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена речце'
        verbose_name_plural = 'измене речци'


class Veznik(models.Model):
    tekst = models.CharField(max_length=100)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'везник'
        verbose_name_plural = 'везници'

    def oblici(self) -> list:
        return [self.tekst]

    def osnovni_oblik(self) -> str:
        return self.tekst

    def vrsta_reci(self) -> int:
        return 8

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[8]

    def __str__(self):
        return f'{self.id}: {self.tekst}'


class IzmenaVeznika(models.Model):
    veznik = models.ForeignKey(Veznik, verbose_name='везник', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена везника'
        verbose_name_plural = 'измене везника'


class Zamenica(models.Model):
    nomjed = models.CharField('номинатив', max_length=50)
    genjed = models.CharField('генитив', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'заменица'
        verbose_name_plural = 'заменице'
        ordering = ['id']
        indexes = [
            models.Index(fields=['nomjed'])
        ]

    def __str__(self):
        return f'{self.id}: {self.nomjed}'

    def osnovni_oblik(self) -> str:
        return self.nomjed

    def vrsta_reci(self) -> int:
        return 5

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[5]

    def oblici(self) -> list:
        retval = _svi_oblici_zamenice(self)
        for v in self.varijantazamenice_set.all():
            retval.extend(_svi_oblici_zamenice(v))
        return retval


class VarijantaZamenice(models.Model):
    zamenica = models.ForeignKey(Zamenica, verbose_name='заменица', on_delete=models.CASCADE)
    redni_broj = models.PositiveSmallIntegerField('редни број')
    nomjed = models.CharField('номинатив', max_length=50, blank=True, null=True)
    genjed = models.CharField('генитив', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'варијанта заменице'
        verbose_name_plural = 'варијанте заменица'


class IzmenaZamenice(models.Model):
    zamenica = models.ForeignKey(Zamenica, verbose_name='заменица', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена заменице'
        verbose_name_plural = 'измене заменица'


def _svi_oblici_zamenice(imenica):
    retval = []
    for x in ['nomjed', 'genjed', 'datjed', 'akujed', 'vokjed', 'insjed', 'lokjed']:
        _append_attr(retval, imenica, x)
    return retval


class Broj(models.Model):
    nomjed = models.CharField('номинатив једнине', max_length=50, blank=True, null=True)
    genjed = models.CharField('генитив једнине', max_length=50, blank=True, null=True)
    datjed = models.CharField('датив једнине', max_length=50, blank=True, null=True)
    akujed = models.CharField('акузатив једнине', max_length=50, blank=True, null=True)
    vokjed = models.CharField('вокатив једнине', max_length=50, blank=True, null=True)
    insjed = models.CharField('инструментал једнине', max_length=50, blank=True, null=True)
    lokjed = models.CharField('локатив једнине', max_length=50, blank=True, null=True)
    nommno = models.CharField('номинатив множине', max_length=50, blank=True, null=True)
    genmno = models.CharField('генитив множине', max_length=50, blank=True, null=True)
    datmno = models.CharField('датив множине', max_length=50, blank=True, null=True)
    akumno = models.CharField('акузатив множине', max_length=50, blank=True, null=True)
    vokmno = models.CharField('вокатив множине', max_length=50, blank=True, null=True)
    insmno = models.CharField('инструментал множине', max_length=50, blank=True, null=True)
    lokmno = models.CharField('локатив множине', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'број'
        verbose_name_plural = 'бројеви'
        ordering = ['id']
        indexes = [
            models.Index(fields=['nomjed'])
        ]

    def __str__(self):
        return f'{self.id}: {self.nomjed}'

    def osnovni_oblik(self) -> str:
        return self.nomjed

    def vrsta_reci(self) -> int:
        return 9

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[9]

    def oblici(self) -> list:
        retval = []
        if self.nomjed:
            retval.append(self.nomjed)
        if self.genjed:
            retval.append(self.genjed)
        if self.datjed:
            retval.append(self.datjed)
        if self.akujed:
            retval.append(self.akujed)
        if self.vokjed:
            retval.append(self.vokjed)
        if self.insjed:
            retval.append(self.insjed)
        if self.lokjed:
            retval.append(self.lokjed)
        if self.nommno:
            retval.append(self.nommno)
        if self.genmno:
            retval.append(self.genmno)
        if self.datmno:
            retval.append(self.datmno)
        if self.akumno:
            retval.append(self.akumno)
        if self.vokmno:
            retval.append(self.vokmno)
        if self.insmno:
            retval.append(self.insmno)
        if self.lokmno:
            retval.append(self.lokmno)
        return retval


class IzmenaBroja(models.Model):
    broj = models.ForeignKey(Broj, verbose_name='број', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена броја'
        verbose_name_plural = 'измене бројева'


class Prilog(models.Model):
    komparativ = models.CharField('компаратив', max_length=50, blank=True, null=True)
    superlativ = models.CharField('суперлатив', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)
    vlasnik = models.ForeignKey(UserProxy, verbose_name='креатор', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'прилог'
        verbose_name_plural = 'прилози'
        ordering = ['id']
        indexes = [
            models.Index(fields=['komparativ']),
            models.Index(fields=['superlativ'])
        ]

    def __str__(self):
        return f'{self.id}: {self.komparativ}'

    def osnovni_oblik(self) -> str:
        return self.komparativ

    def vrsta_reci(self) -> int:
        return 3

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[3]

    def oblici(self) -> list:
        retval = []
        if self.komparativ:
            retval.append(self.komparativ)
        if self.superlativ:
            retval.append(self.superlativ)
        return retval


class IzmenaPriloga(models.Model):
    prilog = models.ForeignKey(Prilog, verbose_name='прилог', on_delete=models.CASCADE)
    operacija_izmene = models.PositiveSmallIntegerField('операција измене', choices=OPERACIJE_IZMENE)
    user = models.ForeignKey(UserProxy, verbose_name='корисник', on_delete=models.DO_NOTHING)
    vreme = models.DateTimeField('време', default=now)

    class Meta:
        verbose_name = 'измена прилога'
        verbose_name_plural = 'измене прилога'
