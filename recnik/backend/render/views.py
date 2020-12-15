import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from xhtml2pdf import pisa

FAKE_ODREDNICE = {
    1: '<b>аба̀жӯр,</b> -у́ра м фр. <i>заклон, штит на лампи, светиљци, сенило.</i>',
    2: '<b>а̀бак(ус)</b> м лат. архит. <i>четвртаста плоча на капителу стуба.</i>',
    3: '<b>абдика́ција</b> ж лат. <i>одрицање од престола, владарства, ређе oд дpyгoг високог звања, оставка на положај, звање.</i>',
    4: '<b>а̏бдикацио̄нӣ</b> (абдика́цӣјскӣ), -а̄, -о̄ <i>која се односи на абдикацију.</i>',
    5: '<b>абдици́рати,</b> -ѝцӣра̄м евр. (несвр.) <i>oдpeћи се (одрицати се) престола или неког високог положаја; oдpeћи се (одрицати се) неког права, уверења и сл.</i>',
    6: '<b>абера́ција</b> ж лат: <b>1.</b> <b>а.</b> астр. <i>привидна промена положаја звезда условљена 3емљиним кретањем и брзином ширења светлости.</i> <b>б.</b> <i>у оптици, одступање преломљених светлосних зракова oд пожељног правца. <b>2.</b> биол. одступање oд типичног облика.</i> <b>3.</b> фиг. <i>скретање, застрањивање.</i>',
    7: '<b>абеце́да</b> ж <b>1.</b> <i>слова латинице (као целовит систем) поређана по утврђеном peдy; уп. азбука и алфабет.</i> <b>2.</b> фиг. <i>основна знања из нечега.</i>',
    8: '<b>абецѐда̄р,</b> -а́ра м лат. <b>1.</b> <b>а.</b> <i>попис по абецедном peдy, абецедни списак.</i> <b>б.</b> <i>слова неког писма исписана по абецедном peдy: глагољски абецедари.</i> <b>2.</b> <i>буквар (латинички).</i>',
    9: '<b>абецѐда̄ријум</b> (абецѐда̄рӣј, -ија) м <i>абецедар (1).</i>',
    10: '<b>а̏бецеда̄рнӣ</b> и <b>абецѐда̄рнӣ</b>, -а̄, -о̄ <i>који се односи на абецедap; фиг. почетнички, основни.</i>',
    11: '<b>абѐце̄днӣ</b> и <b>а̏беце̄днӣ</b>, -а̄, -о̄ <i>који се односи на абецеду, сре­ђен по абецеди:</i> ~ списак, ~ ред.',
    12: '<b>абѐце̄дно</b> и <b>а̏беце̄дно</b> прил. <i>по абецедном peдy:</i> ~ поређати.',
    13: '<b>а̏блатӣв</b> м лат. лингв. <i>падеж за означавање одвајања, потицања и сл. (нпр. у латинском језику).</i>',
    14: '<b>а̏блатӣвнӣ</b>, -а̄, -о̄ <i>који се односи на аблатив:</i> ~ генитив, ~ значење.',
    15: '<b>а̏блендовати</b> и <b>а̀блендовати</b>, -дује̄м свр. и несвр. нем. <i>наизменично, у кратким интервалима палити и гасити фарове аутомобила (најчешће као упозорење или поздрав возачу који дола­зи у сусрет).</i>',
    16: '<b>а̏бнорма̄лан</b>, -лна, -о лат. <i>ненормалан, луд; нездрав, наказан; нeпpиpoдaн:</i> ~ човек; ~ прохтев.',
    17: '<b>а̏бнорма̄лно</b> прил. <i>на абнормалан начин, нeпpиродно:</i> ~ се понашати.',
    18: '<b>абнорма́лно̄ст</b>, -ости ж <i>особина и стање онога који је абнормалан, oнoгa што је абнормално, абнормално стање.</i>',
    19: '<b>аболи́рати</b>, -о̀лӣра̄м cвр. (несвр.) правн. <i>обуставити (обустављати) судски поступак; укинути (укиgати) неку gруштвену институцију или праксу.</i>',
    20: '<b>аболи́ција</b> ж лат. правн. <b>1.</b> <i>обустава кривичног поступка, ослобађање og кривичног гоњења.</i> <b>2.</b> <i>укиgање неке gруштвене институције или праксе (ропства, смртне казне, законске норме и сл.).</i>',
    21: '<b>аболи́цӣјскӣ</b> и <b>а̏болицио̄нӣ</b>, -а̄, -о̄ <i>који се односи на аболицију:</i> ~ поступак.',
    22: '<b>аболиционѝзам</b>, -зма м ист. <i>покрет за укидање ропства; покрет за укидање неког закона.</i>',
    23: '<b>аболицио̀нист(а),</b> -е̄ м (ми. -сти) <i>поборник аболиционизма.</i>',
    24: '<b>аболиционѝстичкӣ,</b> -а̄, -о̄ <i>који се односи на аболиционизам.</i>',
    25: '<b>або̀нент</b> м нем. <i>претплатник.</i>',
    26: '<b>або̀ненткиња</b> ж <i>претплатница.</i>',
    27: '<b>або̀нентскӣ,</b> -а̄, -о̄ <i>који се односи на абоненте:</i> ~ бон.',
    28: '<b>або̀нос</b> и <b>а̏бонос</b> м бот. <i>тропско дрво велике тврдоће Diospyros ebenum.</i>',
    29: '<b>або̀носнӣ</b> и <b>а̏боноснӣ,</b> -а̄, -о̄ <i>који је oд абоноса; који је као абонос:</i> ~ сто; ~ лице.',
}


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    if uri.startswith('/fonts'):
        base_name = os.path.basename(uri)
        file_name = os.path.join(settings.BASE_DIR, 'static', 'fonts', base_name)
        return file_name

    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    else:
        s_url = settings.STATIC_URL  # Typically /static/
        s_root = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        m_url = settings.MEDIA_URL  # Typically /media/
        m_root = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(m_url):
            path = os.path.join(m_root, uri.replace(m_url, ""))
        elif uri.startswith(s_url):
            path = os.path.join(s_root, uri.replace(s_url, ""))
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (s_url, m_url))
    return path


def odrednica_html(request, pk):
    try:
        text = mark_safe(FAKE_ODREDNICE[pk])
        return HttpResponse(text)
    except KeyError:
        return HttpResponseNotFound()


def odrednice_html(request):
    keys = sorted(FAKE_ODREDNICE.keys())
    odrednice = [FAKE_ODREDNICE[key] for key in keys]
    return render(request, 'render/html/odrednice.html', context={'odrednice': odrednice})


def odrednice_pdf(request):
    keys = sorted(FAKE_ODREDNICE.keys())
    odrednice = [FAKE_ODREDNICE[key] for key in keys]
    context = {'odrednice': odrednice}
    template = get_template('render/pdf/odrednice.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="odrednice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
