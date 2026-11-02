[← Sarrera eta helburuak](00-sarrera.md) | [Aurkibidea](index.md) | [1. fasea: Elasticsearch →](01-fasea-elasticsearch.md)

# 0. fasea: sistema prestatu eta Elastic biltegia

Hasi aurretik, Ubuntu LTS edo Linux Mint duen ordenagailu bat behar duzue (sudo baimenekin): gutxienez 4 CPU, 8 GB RAM eta 50 GB disko libre. Gutxienez 4 GB RAM-ekin Elasticsearch abiatzen da, baina Kibana eta Logstash gehituta oso justu dabil.

1.  Sistema eguneratu eta tresna oinarrizkoak instalatu:

- sudo apt update && sudo apt upgrade -y
      sudo apt install -y curl wget gnupg apt-transport-https jq python3 python3-venv python3-pip

2.  Baliabideak egiaztatu eta ordenagailuaren IP helbidea idatzi (geroago behar duzue; `hostname -I` komandoak lehenengo IP-a ematen du, eta Docker-en sareak ere ager daitezke). Azken komandoak (`ss`) ez du ezer erakutsi behar: bestela, 80, 5000, 5044, 5601 edo 9200 portuaren bat okupatuta dago. Docker edukiontziak badituzu Elasticsearch edo Kibana-rekin, gelditu `docker stop $(docker ps -q)` komandoarekin jarraitu aurretik:

- nproc
      free -h
      df -h /
      hostname -I
      sudo ss -tlnp | grep -E ':(80|5000|5044|5601|9200)\b'

3.  Elastic-en GPG gakoa eta APT biltegia gehitu:

- wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

      echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/9.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-9.x.list

      sudo apt update

4.  Instalatuko den bertsioa begiratu:

- apt-cache policy elasticsearch | head -4

**Arau garrantzitsua:** osagai guztiek (Elasticsearch, Kibana, Logstash, Filebeat, Heartbeat) bertsio nagusi eta txiki bera izan behar dute. Bertsio desberdinek akats arraroak sortzen dituzte.

**Egiaztapena:** `apt-cache policy elasticsearch` komandoak “Candidate” lerroan bertsio bat erakutsi behar du. Idatzi zure koadernoan.

---
[← Sarrera eta helburuak](00-sarrera.md) | [Aurkibidea](index.md) | [1. fasea: Elasticsearch →](01-fasea-elasticsearch.md)
