## Potrebne stvari
 * Python
 * ElasticSearch-DSL

## Podešavanje za razvoj

Kreiranje virtuelnog okruženja:
```bash
python3 -m venv ~/path/to/new/venv
source ~/path/to/new/venv/bin/activate
```

Instaliranje potrebnih paketa
```bash
pip install -r requirements.txt
```

## Pravljenje Docker slike za ElasticSearch

Iz `indexer` foldera:
```bash
docker build -t es-sr-lat .
```

## Pokretanje ElasticSearch-a:
```bash
docker run -p 9200:9200 -p 9300:9300 --name "es-sr-lat" -e "discovery.type=single-node" es-sr-lat
```

## Pokretanje aplikacije:
```bash
python3 app.py
```
Aplikacija je samo za testiranje, model dokumenta, indeks i funkcija za pretragu ce biti prebacene na odgovarajuca mesta na backendu.
Moguce je prilikom prvog pokretanja da se ne dobiju rezultati jer ElasticSearch nije zavrsio indeksiranje, u tom slucaju pokrenuti jos jednom.

Pokretanje Kibane:
```bash
docker pull docker.elastic.co/kibana/kibana:7.4.0
docker run --link es-sr-lat:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.4.0
```

Chrome plugin za ElasticSearch preko kojeg se mogu kreirati/brisati indeksi, dokumenti, i izvrsavati pretraga:
https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm

Originalni repozitorijum za Serbian plugin: 
https://github.com/chenejac/udd06