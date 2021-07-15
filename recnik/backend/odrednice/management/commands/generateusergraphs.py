from datetime import datetime, timedelta
import json
import logging
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.timezone import now, make_aware
from odrednice.models import StatistikaUnosa, UserProxy, GrafikonUnosa

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate graphs for users'

    def handle(self, *args, **options):
        log.info('Generisanje grafikona obradjivaca...')

        # izracunaj datume za nedelje izmedju pocetnog i krajnjeg datuma
        start_date = make_aware(datetime(2021, 5, 1, 23, 59))
        end_date = now()
        log.info(f'Pocetni datum: {start_date.strftime("%Y-%m-%d %H:%M")}')
        log.info(f'Krajnji datum: {end_date.strftime("%Y-%m-%d %H:%M")}')
        first_sunday = start_date + timedelta(7 - ((start_date.weekday() + 1) % 7))
        last_sunday = end_date - timedelta((end_date.weekday() + 1) % 7)
        last_sunday = last_sunday.replace(hour=23, minute=59)
        sundays = []
        sunday = first_sunday
        while True:
            sundays.append(sunday)
            sunday = sunday + timedelta(days=7)
            if sunday > last_sunday:
                break

        # pokupi najsveziju statistiku za svaku nedelju
        users = UserProxy.objects.all()
        source_data = []
        for sunday in sundays:
            statistika_unosa = StatistikaUnosa.objects.filter(vreme__lt=sunday).order_by('-vreme').first()
            if not statistika_unosa:
                continue
            source_item = {
                'date': sunday,
                'week': sunday.strftime('%U'),
                'users': {u.puno_ime(): {'broj_odrednica': 0, 'broj_znakova': 0, 'zavrsenih_odrednica': 0, 'zavrsenih_znakova': 0} for u in users}
            }
            for stavka in statistika_unosa.stavkastatistikeunosa_set.all():
                i = source_item['users'][stavka.user.puno_ime()]
                i['broj_odrednica'] = stavka.broj_odrednica
                i['broj_znakova'] = stavka.broj_znakova
                i['zavrsenih_odrednica'] = stavka.zavrsenih_odrednica
                i['zavrsenih_znakova'] = stavka.zavrsenih_znakova
            source_data.append(source_item)

        # ukloni neaktivne korisnike (oni koji u poslednjoj nedelji nemaju nista uneto)
        inactive_users = []
        last_item = source_data[-1]
        for user in last_item['users'].keys():
            if last_item['users'][user]['broj_odrednica'] == 0:
                inactive_users.append(user)
                log.info(f'Neaktivan korisnik za grafikon: {user}')
        for item in source_data:
            for iu in inactive_users:
                del item['users'][iu]

        data = json.dumps(source_data, cls=DjangoJSONEncoder)
        chart = json.dumps(self._for_chart(source_data), cls=DjangoJSONEncoder)
        GrafikonUnosa.objects.update_or_create(tip=4, defaults={'data': data, 'chart': chart})

        # preracunaj brojeve kao razlike u odnosu na prethodnu nedelju
        for i in range(len(source_data)-1, 0, -1):
            current = source_data[i]
            previous = source_data[i-1]
            self._subtract(current, previous)

        data = json.dumps(source_data, cls=DjangoJSONEncoder)
        chart = json.dumps(self._for_chart(source_data), cls=DjangoJSONEncoder)
        GrafikonUnosa.objects.update_or_create(tip=1, defaults={'data': data, 'chart': chart})

        self.style.SUCCESS(f'Uspesno generisan grafikon ID: ')
        log.info('Generisanje grafikona zavrseno.')

    def _subtract(self, current, previous):
        for user in current['users'].keys():
            for field in ['broj_odrednica', 'broj_znakova', 'zavrsenih_odrednica', 'zavrsenih_znakova']:
                current['users'][user][field] = current['users'][user][field] - previous['users'][user][field]

    def _for_chart(self, data):
        labels = [item['date'].strftime('%Y-%m-%d') for item in data]
        datasets = []
        for user in data[0]['users'].keys():
            dataset = {'label': user, 'data': []}
            for item in data:
                dataset['data'].append(item['users'][user])
            datasets.append(dataset)
        return {'labels': labels, 'datasets': datasets}
