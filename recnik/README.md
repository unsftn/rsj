## Potrebne stvari

Za backend:
 * Python 3.11
 * MariaDB 10.10+
 * Elasticsearch 8.12+

Za frontend:
 * Node.js 20
 * Angular 17
 * PrimeNG 17

## Podešavanje za razvoj

Kreiranje virtuelnog okruženja:
```bash
python3 -m venv ~/path/to/new/venv
source ~/path/to/new/venv/bin/activate
```

MySQL baza podataka mora biti podešena tako da postoji
korisnik `recnik` sa lozinkom `recnik` sa svim pravima
na šemi `recnik`:
```
mysql -u root
mysql> CREATE DATABASE recnik CHARACTER SET utf8mb4;
mysql> CREATE USER 'recnik'@'localhost' IDENTIFIED BY 'recnik';
mysql> GRANT ALL PRIVILEGES ON recnik.* TO 'recnik'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Sve naredne operacije obavljaju se iz korenskog direktorijuma Django
projekta, dakle `recnik/backend`.

Instaliranje potrebnih paketa
```bash
pip install -r requirements.txt
```

Migracija baze na poslednju verziju:
```bash
python manage.py migrate
```

Pokretanje testova:
```bash
python manage.py test
```

Pokretanje razvojnog servera:
```bash
python manage.py runserver
```

Pokretanje frontend servera iz korenskog direktorijuma Angular
projekta, dakle `recnik/frontend`:
```bash
ng serve
```

## Instalacija na produkciju

```bash
mkdir -p /var/dockersites
cd /var/dockersites
git clone https://github.com/unsftn/rsj.git
cd rsj/recnik
docker network create recnik
docker network connect recnik traefik
mkdir data init elastic export private log media
touch private/secrets
# inicijalizuj promenljive u private/secrets
docker compose up -d --build
```

Značenje direktorijuma je sledeće:
* `data`: fajlovi MariaDB baze podataka
* `init`: inicijalni skriptovi za bazu podataka (pokreću se samo prvi put, kada baza nije kreirana)
* `elastic`: fajlovi za Elasticsearch
* `export`: direktorijum koji se mapira na /app/export i mogu mu pristupati Django komande
* `private`: sadrži fajl secrets sa lozinkama i drugim podešavanjima
* `media`: uploadovani fajlovi, generisani fajlovi
* `log`: log fajlovi
