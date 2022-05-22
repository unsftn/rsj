# -*- coding: utf-8 -*-
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
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)

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

    class Meta:
        verbose_name = 'придев'
        verbose_name_plural = 'придеви'
        ordering = ['id']
        indexes = [
            models.Index(fields=['lema'])
        ]

    def __str__(self):
        return f'{self.id}'

    def osnovni_oblik(self) -> str:
        return self.lema

    def vrsta_reci(self) -> int:
        return 2

    def naziv_vrste_reci(self) -> str:
        return VRSTE_RECI[2]

    def oblici(self) -> list:
        return _svi_oblici_prideva(self)


class VidPrideva(models.Model):
    pridev = models.ForeignKey(Pridev, verbose_name='придев', on_delete=models.CASCADE)
    vid = models.IntegerField('вид', choices=PRIDEVSKI_VID)
    mnomjed = models.TextField('мушки номинатив једнина', blank=True, null=True)
    mgenjed = models.TextField('мушки генитив једнина', blank=True, null=True)
    mdatjed = models.TextField('мушки датив једнина', blank=True, null=True)
    makujed = models.TextField('мушки акузатив једнина', blank=True, null=True)
    mvokjed = models.TextField('мушки вокатив једнина', blank=True, null=True)
    minsjed = models.TextField('мушки инструментал једнина', blank=True, null=True)
    mlokjed = models.TextField('мушки локатив једнина', blank=True, null=True)
    mnommno = models.TextField('мушки номинатив множина', blank=True, null=True)
    mgenmno = models.TextField('мушки генитив множина', blank=True, null=True)
    mdatmno = models.TextField('мушки датив множина', blank=True, null=True)
    makumno = models.TextField('мушки акузатив множина', blank=True, null=True)
    mvokmno = models.TextField('мушки вокатив множина', blank=True, null=True)
    minsmno = models.TextField('мушки инструментал множина', blank=True, null=True)
    mlokmno = models.TextField('мушки локатив множина', blank=True, null=True)
    znomjed = models.TextField('женски номинатив једнина', blank=True, null=True)
    zgenjed = models.TextField('женски генитив једнина', blank=True, null=True)
    zdatjed = models.TextField('женски датив једнина', blank=True, null=True)
    zakujed = models.TextField('женски акузатив једнина', blank=True, null=True)
    zvokjed = models.TextField('женски вокатив једнина', blank=True, null=True)
    zinsjed = models.TextField('женски инструментал једнина', blank=True, null=True)
    zlokjed = models.TextField('женски локатив једнина', blank=True, null=True)
    znommno = models.TextField('женски номинатив множина', blank=True, null=True)
    zgenmno = models.TextField('женски генитив множина', blank=True, null=True)
    zdatmno = models.TextField('женски датив множина', blank=True, null=True)
    zakumno = models.TextField('женски акузатив множина', blank=True, null=True)
    zvokmno = models.TextField('женски вокатив множина', blank=True, null=True)
    zinsmno = models.TextField('женски инструментал множина', blank=True, null=True)
    zlokmno = models.TextField('женски локатив множина', blank=True, null=True)
    snomjed = models.TextField('средњи номинатив једнина', blank=True, null=True)
    sgenjed = models.TextField('средњи генитив једнина', blank=True, null=True)
    sdatjed = models.TextField('средњи датив једнина', blank=True, null=True)
    sakujed = models.TextField('средњи акузатив једнина', blank=True, null=True)
    svokjed = models.TextField('средњи вокатив једнина', blank=True, null=True)
    sinsjed = models.TextField('средњи инструментал једнина', blank=True, null=True)
    slokjed = models.TextField('средњи локатив једнина', blank=True, null=True)
    snommno = models.TextField('средњи номинатив множина', blank=True, null=True)
    sgenmno = models.TextField('средњи генитив множина', blank=True, null=True)
    sdatmno = models.TextField('средњи датив множина', blank=True, null=True)
    sakumno = models.TextField('средњи акузатив множина', blank=True, null=True)
    svokmno = models.TextField('средњи вокатив множина', blank=True, null=True)
    sinsmno = models.TextField('средњи инструментал множина', blank=True, null=True)
    slokmno = models.TextField('средњи локатив множина', blank=True, null=True)

    class Meta:
        verbose_name = 'вид придева'
        verbose_name_plural = 'видови придева'
        ordering = ['vid']

    def __str__(self):
        return f'{self.pridev.id}/{self.id}: {self.mnomjed}'


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
    for vid in pridev.vidprideva_set.all():
        for attr in ['mnomjed', 'mgenjed', 'mdatjed', 'makujed', 'mvokjed', 'minsjed', 'mlokjed',
                     'mnommno', 'mgenmno', 'mdatmno', 'makumno', 'mvokmno', 'minsmno', 'mlokmno',
                     'znomjed', 'zgenjed', 'zdatjed', 'zakujed', 'zvokjed', 'zinsjed', 'zlokjed',
                     'znommno', 'zgenmno', 'zdatmno', 'zakumno', 'zvokmno', 'zinsmno', 'zlokmno',
                     'snomjed', 'sgenjed', 'sdatjed', 'sakujed', 'svokjed', 'sinsjed', 'slokjed',
                     'snommno', 'sgenmno', 'sdatmno', 'sakumno', 'svokmno', 'sinsmno', 'slokmno']:
            _append_attr(retval, vid, attr)
    return retval


class Predlog(models.Model):
    tekst = models.CharField(max_length=100)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)

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
    predlog = models.ForeignKey(Predlog, verbose_name='', on_delete=models.CASCADE)
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
    uzvik = models.ForeignKey(Uzvik, verbose_name='', on_delete=models.CASCADE)
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
    recca = models.ForeignKey(Recca, verbose_name='', on_delete=models.CASCADE)
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
    veznik = models.ForeignKey(Veznik, verbose_name='', on_delete=models.CASCADE)
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


class Prilog(models.Model):
    komparativ = models.CharField('компаратив', max_length=50, blank=True, null=True)
    superlativ = models.CharField('суперлатив', max_length=50, blank=True, null=True)
    recnik_id = models.IntegerField('ID одреднице у речнику', blank=True, null=True)
    status = models.ForeignKey(StatusReci, verbose_name='статус речи', on_delete=models.PROTECT, blank=True, null=True)
    vreme_kreiranja = models.DateTimeField('време креирања', default=now)
    poslednja_izmena = models.DateTimeField('време последње измене', default=now)

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


