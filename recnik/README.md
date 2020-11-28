## Potrebne stvari

Za backend:
 * Python
 * Django
 * uWSGI
 * MySQL 5.7+ ili MariaDB 10+

Za frontend:
 * Angular 11
 * PrimeNG 11

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
mysql> CREATE DATABASE recnik CHARACTER SET utf8;
mysql> CREATE USER 'recnik'@'localhost' IDENTIFIED BY 'recnik';
mysql> GRANT ALL PRIVILEGES ON recnik.* TO 'recnik'@'localhost';
mysql> FLUSH PRIVILEGES;
```

Sve naredne operacije obavljaju se iz korenskog direktorijuma Django
projekta, dakle `recnik-backend/app`.

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

Pokretanje frontend servera:
```bash
ng serve
```

## Pravljenje Docker slike

Iz `recnik-backend` foldera:
```bash
docker build -t rsj/recnik .
```

Pokretanje MySQL-a:
```bash
docker run \
  --name recnik-mysql \
  --restart always \
  --detach \
  -v /var/rsj/recnik/db/data:/var/lib/mysql \
  -v /var/rsj/recnik/db/init:/docker-entrypoint-initdb.d \
  -e MYSQL_ROOT_PASSWORD=recnik \
  -e MYSQL_USER=recnik \
  -e MYSQL_PASSWORD=recnik \
  -e MYSQL_DATABASE=recnik \
  mysql:5.7.21
```

Pokretanje aplikacije:
```bash
docker run \
  --name recnik \
  --detach \
  --link recnik-mysql \
  -v /var/rsj/recnik/private:/private \
  -v /var/rsj/recnik/log:/app/log \
  -p 8000:8000 \
  rsj/recnik
```
