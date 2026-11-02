[← 3. fasea: web simulatua](03-fasea-web.md) | [Aurkibidea](index.md) | [5. fasea: B bidea, Logstash eta datuen garbiketa →](05-fasea-B-logstash.md)

# 4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era

Helburua: Filebeat-ek 10 segundoro API-a kontsultatu eta sentsore-irakurketa bakoitza dokumentu independente gisa bidaltzea `sentsoreak-beats` indizera. Logstash gabe, eta datuak garbitu gabe.

1.  Filebeat instalatu:

- sudo apt install -y filebeat

2.  Pasahitza testu argian idatzi ez dezazuen, gorde Filebeat-en keystore-an (komandoak pasahitza eskatuko dizu):

- sudo filebeat keystore create
      sudo filebeat keystore add ES_PASSWORD

  Gero konfigurazioan `${ES_PASSWORD}` idatziz erabil dezakezue.

3.  Egin jatorrizko konfigurazioaren kopia eta idatzi `/etc/filebeat/filebeat.yml` berria:

- sudo cp /etc/filebeat/filebeat.yml /etc/filebeat/filebeat.yml.orig
      sudo nano /etc/filebeat/filebeat.yml

**Konfigurazioak izan behar duena:**

- `httpjson` motako sarrera bat, `http://localhost/api/sentsoreak` helbidera, 10 segundoko tartearekin.
- `response.split` bidez, erantzunaren `sentsoreak` zerrendako elementu bakoitza ebento bakar bihurtzea. Pista: erantzunaren gorputza `body` izenarekin heldu zaio helburuari.
- Ebentoaren `message` eremuan JSON testua dator. Dekodetu `decode_json_fields` prozesadorearekin, eremuak erro mailan jarriz (`target: ""`), eta gero kendu `message` (`drop_fields`).
- Irteera: `output.elasticsearch`, HTTPS bidez, `/etc/elastic-ca/http_ca.crt` CA ziurtagiriarekin, `elastic` erabiltzailearekin eta keystore-ko pasahitzarekin.
- Indizearen izena `sentsoreak-beats` izateko, `output.elasticsearch.index` ez da aski: `setup.template.name`, `setup.template.pattern` eta `setup.ilm.enabled: false` ere behar dira.

Irtenbidea ez begiratu lehenik. Erabili `filebeat.reference.yml` fitxategia (`/etc/filebeat/filebeat.reference.yml`) eta Elastic-en dokumentazioa.

**Eskema (lagungarria).** Bete `???` hutsuneak; egitura eta sangria ematen dizkizuet, baina kontzeptuak zuek jarri behar dituzue. Fitxategi gisa ere badago (`filebeat.esqueleto.yml`).

    # A BIDEA: ESKEMA. Bete ??? hutsuneak. Fitxategia: /etc/filebeat/filebeat.yml
    filebeat.inputs:
      - type: ???                  # API HTTP bat kontsultatzeko sarrera-mota
        id: sentsoreak-api
        interval: ???
        request.url: ???
        request.method: GET
        response.split:
          target: ???              # zerrenda duen eremua ("body." aurrizkiarekin)
          type: array
        processors:
          - decode_json_fields:
              fields: ["message"]
              target: ???          # "" = eremuak dokumentuaren erro mailan
              overwrite_keys: true
              add_error_key: true
          - drop_fields:
              fields: [???]        # dagoeneko behar ez den eremua
              ignore_missing: true

    setup.ilm.enabled: ???         # true edo false: zergatik?
    setup.template.name: ???
    setup.template.pattern: ???

    output.elasticsearch:
      hosts: ["https://localhost:9200"]
      username: "elastic"
      password: "${ES_PASSWORD}"
      ssl.certificate_authorities: [???]            # CA ziurtagiriaren bidea
      index: ???

4.  Konfigurazioa eta konexioa probatu abiarazi aurretik:

- sudo filebeat test config -e
      sudo filebeat test output

5.  Abiarazi eta log-ak jarraitu:

- sudo systemctl enable --now filebeat
      sudo journalctl -u filebeat -f

**Egiaztapena:** minutu batera, Kibana Dev Tools-en:

    GET sentsoreak-beats/_count
    GET sentsoreak-beats/_search?size=3
    GET sentsoreak-beats/_mapping

Irakurketak ikusi behar dituzue `sentsore_id`, `mota`, `balioa`, `zona` eta abar eremuekin. Kontsulta bakoitzak 9 dokumentu gehitu behar ditu (sentsore bakoitzeko bat), hau da, 10 segundoro 9 dokumentu berri. Kontuz: Filebeat 9-k \*data stream\* bat sortzen du; `_cat/indices` komandoan `.ds-sentsoreak-beats-...` izenarekin ikusiko duzue, baina `sentsoreak-beats` izenarekin kontsultatu dezakezue.

**2. galdera:** zein motatakoa da `balioa` eremua mapaketan? Zergatik hori, eta ez beste bat? (Pista: Elasticsearch-ek lehen dokumentuan oinarritzen da.)

**3. galdera:** begiratu Filebeat-en log-ak (`sudo journalctl -u filebeat -n 50 --no-pager`). Zer abisu ikusten duzue? Egiaztatu `_count` bidez ea dokumenturik falta den; gero, erreproduzitu errorea eskuz Dev Tools-en eta idatzi errorearen izena eta zein balioak eragin duen. Filebeat-en log-ak `events were dropped` abisua ematen du, baina ez du arrazoia erakusten:

    POST sentsoreak-beats/_doc
    { "@timestamp": "2026-11-02T11:30:00Z", "sentsore_id": "proba", "balioa": "N/A" }

**4. galdera:** exekutatu hau eta azaldu zer erakusten duen. Zergatik da arazo bat Beats bidea soilik erabiltzean?

    GET sentsoreak-beats/_count
    { "query": { "range": { "balioa": { "lt": -100 } } } }

**5. galdera:** begiratu `_mapping` erantzunean: zein motatakoa da `denbora` eremua? Zein eremu erabiltzen du Kibana-k denbora-iragazkirako, eta zer ordu adierazten du: sentsorearena ala Filebeat-ek irakurri duena?

---
[← 3. fasea: web simulatua](03-fasea-web.md) | [Aurkibidea](index.md) | [5. fasea: B bidea, Logstash eta datuen garbiketa →](05-fasea-B-logstash.md)
