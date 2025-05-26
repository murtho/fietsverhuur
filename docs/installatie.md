# Installatie

Dit project maakt gebruik van Python. Daarnaast dienen een aantal packages geïnstalleerd te worden.

In het `requirements.txt` bestand staan de dependencies. Installeer deze packages met behulp van `pip` of gebruik een IDE zoals `pycharm` met geautomatiseerde tools om de packages te installeren.

Naast Python dient er een verbinding gelegd te worden met een mysql database.
De configuratie daarvoor dient opgezet te worden

Kopieer en hernoem het bestand `.env.dist` naar `.env` en vul je eigen database credentials in.
Deze database credentials dien je ook in te vullen tijdens het aanmaken van de mysql database
Let dus op dat je de gegevens ook in het onderstaande script aanpast.

In de map `\docs\sql\` staat een [create script](/docs/sql/create.sql) om de database aan te maken. 
Ook staat er een [insert script](/docs/sql/insert.sql) om de database te vullen.