[← 6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch](06-fasea-C-filebeat-logstash.md) | [Aurkibidea](index.md) | [8. fasea: egiaztapena eta Kibana dashboard-a →](08-fasea-dashboard.md)

# 7. fasea: D bidea, Heartbeat eta eskuragarritasuna

A, B eta C bideek datuak (irakurketak, log-ak) ekartzen dituzte. Heartbeat-ek, berriz, **zerbitzua bizirik dagoen** neurtzen du: 10 segundoro web simulatua kontsultatzen du eta erantzun-denbora eta egoera (`up` edo `down`) gordetzen ditu.

1.  Heartbeat instalatu. Kontuz, Elastic-en paketearen izena `heartbeat-elastic` da:

- sudo apt install -y heartbeat-elastic

2.  Pasahitza keystore-an gorde:

- sudo heartbeat keystore create
      sudo heartbeat keystore add ES_PASSWORD

3.  **Konfigurazioa idatzi:** `/etc/heartbeat/heartbeat.yml` (egin kopia lehenik). Behar duena:

    - `http` monitore bat `/osasuna` helbidearentzat, 10 segundoz behin, `200` egoera-kodea itxaroten duena.
    - `http` monitore bat `/api/sentsoreak` helbidearentzat, 30 segundoz behin.
    - `tcp` monitore bat Elasticsearch-en `9200` portuarentzat, 30 segundoz behin.
    - Monitore bakoitzak `id` eta `name` propioa.
    - `output.elasticsearch`: A bideko ezarpen berdinak (HTTPS, CA, `elastic`, keystore). Ez jarri `index`: Heartbeat-en lehenetsitako data stream-a erabiliko da (`heartbeat-*`).

4.  Probatu eta abiarazi (`test config -e`-k log asko erakusten du; bilatu `Config OK` lerroa):

- sudo heartbeat test config -e
      sudo heartbeat test output
      sudo systemctl enable --now heartbeat-elastic
      sudo journalctl -u heartbeat-elastic -f

**Egiaztapena:**

    GET heartbeat-*/_search?size=3
    GET heartbeat-*/_search
    { "size": 0, "aggs": { "egoera": { "terms": { "field": "monitor.status" } } } }

Ikusi behar dituzue `monitor.name`, `monitor.status`, `monitor.duration.us` eta `url.full` eremuak.

**Erorketa-proba.** Web simulatua gelditu bi minutuz eta berriz piztu:

    sudo systemctl stop web-sentsoreak
    # itxaron 2 minutu
    sudo systemctl start web-sentsoreak

Gero begiratu `monitor.status: down` duten dokumentuak, `error.message` eremuarekin (Discover-en, `heartbeat-*` data view-a sortuta). Kontuz: `error.message` eremua ezin da `terms` agregazioarekin taldekatu (`match_only_text` mota du); erabili `_source` iragazkia edo `filter_path`.

**12. galdera:** zer esan nahi dute `monitor.status` eta `monitor.duration.us` eremuek? Zergatik agertzen da tarteka `down` `/osasuna` monitorean, web-a martxan dagoenean ere?

**13. galdera:** web-a gelditu zenuten bi minutuetan, zer ikusi duzue A, B eta C bideetan (hutsuneak, erroreak Filebeat/Logstash-en log-etan, egoera-kode berriak web-logak-\* indizean)? Zein bidek sortu du dokumentu bat “web-a erori da” esanez? Zergatik da hori garrantzitsua monitorizazioan? Gainera: zer gertatuko litzateke B bideko pipeline-ak `_jsonparsefailure` ebentuak baztertuko ez balitu? (Begiratu `sentsoreak-baztertuak` indizea.)

---
[← 6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch](06-fasea-C-filebeat-logstash.md) | [Aurkibidea](index.md) | [8. fasea: egiaztapena eta Kibana dashboard-a →](08-fasea-dashboard.md)
