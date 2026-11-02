[← 0. fasea: sistema prestatu eta Elastic biltegia](00-fasea-sistema.md) | [Aurkibidea](index.md) | [2. fasea: Kibana →](02-fasea-kibana.md)

# 1. fasea: Elasticsearch

Elasticsearch-ek bere JDK-a dakar, ez duzue Java instalatu behar. Instalazioak segurtasuna (HTTPS eta autentifikazioa) automatikoki aktibatzen du.

1.  Instalatu:

- sudo apt install -y elasticsearch

2.  **Instalazioaren bukaeran, pantailan** `elastic` **erabiltzailearen pasahitza agertzen da, behin bakarrik.** Kopiatu eta gorde. Galtzen baduzue, berrezarri (Elasticsearch abiarazita egon behar da, beraz 4. urratsaren ondoren; lehenago `Failed to determine the health of the cluster` errorea ematen du):

- sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

3.  Memoria gutxiko makinetan, mugatu JVM heap-a (RAM-aren erdia gehienez):

- echo -e "-Xms2g\n-Xmx2g" | sudo tee /etc/elasticsearch/jvm.options.d/heap.options

4.  Abiarazi eta sistemarekin batera hasteko konfiguratu:

- sudo systemctl daemon-reload
      sudo systemctl enable --now elasticsearch
      sudo systemctl status elasticsearch

**Oharra:** abiaraztean Java-ren `WARNING` mezuak (`sun.misc.Unsafe`...) normalak dira; garrantzitsua `active (running)` ikustea da. `status` ikuspegitik irteteko, sakatu `q`.

5.  Elasticsearch-en CA ziurtagiria toki irakurgarri batera kopiatu. Beats-ek eta Logstash-ek geroago erabiliko dute (ziurtagiri publikoa da, ez da sekretua):

- sudo mkdir -p /etc/elastic-ca
      sudo cp /etc/elasticsearch/certs/http_ca.crt /etc/elastic-ca/http_ca.crt
      sudo chmod 644 /etc/elastic-ca/http_ca.crt

6.  Pasahitza aldagai batean gorde saio honetarako eta probatu:

- export ELASTIC_PASSWORD='ZURE_PASAHITZA'
      curl --cacert /etc/elastic-ca/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200

**Egiaztapena:** erantzunak JSON bat izan behar du, `cluster_name`, `version.number` eta `tagline` eremuekin. Gero:

    curl --cacert /etc/elastic-ca/http_ca.crt -u elastic:$ELASTIC_PASSWORD "https://localhost:9200/_cluster/health?pretty"

`green` edo `yellow` bada, ondo dago. Nodo bakarrean `yellow` normala da, erreplikak ezin direlako esleitu.

Abiarazten ez bada: `sudo journalctl -u elasticsearch -n 50 --no-pager`.

---
[← 0. fasea: sistema prestatu eta Elastic biltegia](00-fasea-sistema.md) | [Aurkibidea](index.md) | [2. fasea: Kibana →](02-fasea-kibana.md)
