## Potrebne stvari
    Java
    JAVA_HOME=jdk1.8
## Pokretanje aplikacije
Potrebno je napraviti extractor.jar fajl, to se može postići pokretanjem sledeće komande:
```bash
mvn clean install
```
Zatim, potrebno je pokrenuti docker-compose.yml pomoću sledeće komande:
```bash
docker-compose up
```
Aplikacija nakon pokretanja će biti dostupna na portu 8090. 
Za promenu porta, izmeniti docker-compose.yml fajl.

## Pravljenje Docker slike
Potrebno je napraviti extractor.jar fajl, to se može postići pokretanjem sledeće komande:
```bash
mvn clean install
```
Zatim, za pravljenje slike, potrebno je pokrenuti sledeću komandu:
```bash
docker-compose build
```