## Potrebne stvari

Za backend:
 * Python
 * Django
 * uWSGI
 * MySQL 5.7+ ili MariaDB 10+

Za frontend:
 * Angular 12
 * PrimeNG 12

## Podešavanje za razvoj

Kreiranje virtuelnog okruženja:
```bash
python3 -m venv ~/path/to/new/venv
source ~/path/to/new/venv/bin/activate
```

MySQL baza podataka mora biti podešena tako da postoji
korisnik `korpus` sa lozinkom `korpus` sa svim pravima
na šemi `korpus`:
```
mysql -u root
mysql> CREATE DATABASE korpus CHARACTER SET utf8mb4;
mysql> CREATE USER 'korpus'@'localhost' IDENTIFIED BY 'korpus';
mysql> GRANT ALL PRIVILEGES ON korpus.* TO 'korpus'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Sve naredne operacije obavljaju se iz korenskog direktorijuma Django
projekta, dakle `korpus/backend`.

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
projekta, dakle `korpus/frontend`:
```bash
ng serve
```

## Pravljenje Docker slike

Iz `korpus` foldera:
```bash
docker build -t rsj/korpus .
```

Pokretanje MySQL-a:
```bash
docker run \
  --name korpus-mysql \
  --restart always \
  --detach \
  -v /var/rsj/korpus/data:/var/lib/mysql \
  -v /var/rsj/korpus/init:/docker-entrypoint-initdb.d \
  -e MYSQL_ROOT_PASSWORD=korpus \
  -e MYSQL_USER=korpus \
  -e MYSQL_PASSWORD=korpus \
  -e MYSQL_DATABASE=korpus \
  mysql:5.7.32 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci 
```

Pokretanje aplikacije:
```bash
docker run \
  --name recnik \
  --detach \
  --link korpus-mysql \
  -v /var/rsj/korpus/private:/private \
  -v /var/rsj/korpus/log:/app/log \
  -p 8000:8000 \
  rsj/korpus
```

Na laptopu:
```bash
mkdir -p ~/tmp/rsj/data
mkdir -p ~/tmp/rsj/init
mkdir -p ~/tmp/rsj/log
mkdir -p ~/tmp/rsj/private
echo "SECRET_KEY=abcdwfslkdjslkdjg" > ~/tmp/private/secrets
docker run --name korpus-mysql --detach -v ~/tmp/rsj/data:/var/lib/mysql -v ~/tmp/rsj/init:/docker-entrypoint-initdb.d -e MYSQL_ROOT_PASSWORD=korpus -e MYSQL_USER=korpus -e MYSQL_PASSWORD=korpus -e MYSQL_DATABASE=korpus mysql:5.7.32 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci 
docker run --name korpus --detach --link korpus-mysql -v ~/tmp/rsj/private:/private -v ~/tmp/rsj/log:/app/log -p 8000:8000 rsj/korpus
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

Chrome plugin za ElasticSearch preko kojeg se mogu kreirati/brisati indeksi, dokumenti, i izvrsavati pretraga:
https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm
