[← 5. fasea: B bidea, Logstash eta datuen garbiketa](05-fasea-B-logstash.md) | [Aurkibidea](index.md) | [7. fasea: D bidea, Heartbeat eta eskuragarritasuna →](07-fasea-D-heartbeat.md)

# 6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch

Helburua: nginx-ek idazten duen sarbide-log fitxategia (JSON formatuan) Filebeat-ek irakurri eta Logstash-i bidaltzea; Logstash-ek lerro bakoitzeko JSON dekodetu, ordua @timestamp bihurtu eta web-logak-\* indizeetan gordetzea. Hau da ekoizpeneko eredu ohikoena: Beats bidaltzen du, Logstash prozesatzen du.

Log-lerro bat horrelakoa da:

    {"ordua":"2026-11-01T11:46:10+01:00","bezeroa":"127.0.0.1","x_forwarded_for":"","metodoa":"GET","url":"/api/akatsa","egoera_kodea":500,"byteak":27,"erreferentzia":"","user_agent":"curl/8.5.0","erantzun_denbora":0.002}

**Kontuz: Beats-ek irteera bakarra onartzen du.** A biderako Filebeat-ek Elasticsearch-era bidaltzen du eta hemen Logstash-era bidali behar da. Horregatik Filebeat-en **bigarren instantzia** bat erabiliko dugu: konfigurazio-fitxategi propioa, `--path.data` propioa eta zerbitzu propioa.

1.  Bigarren Filebeat-erako zerbitzua sortu (konfigurazioa 3. urratsean idatziko duzue):

- sudo tee /etc/systemd/system/filebeat-logak.service > /dev/null <<'EOF'
      [Unit]
      Description=Filebeat (web-logak -> Logstash)
      After=network-online.target

      [Service]
      ExecStart=/usr/share/filebeat/bin/filebeat --environment systemd -c /etc/filebeat/filebeat-logak.yml --path.home /usr/share/filebeat --path.config /etc/filebeat --path.data /var/lib/filebeat-logak --path.logs /var/log/filebeat-logak
      Restart=always

      [Install]
      WantedBy=multi-user.target
      EOF

      sudo systemctl daemon-reload

2.  Logstash-en pipeline-ak bereizi. Orain arte pipeline bakarra zegoen (`conf.d/*.conf`); bi izango dira, bakoitza bere fitxategiarekin, haien ebentoak nahas ez daitezen. Editatu `/etc/logstash/pipelines.yml`:

- - pipeline.id: sentsoreak-http
        path.config: "/etc/logstash/conf.d/sentsoreak.conf"
      - pipeline.id: web-logak
        path.config: "/etc/logstash/conf.d/web-logak.conf"

3.  **Filebeat-en konfigurazioa idatzi:** `/etc/filebeat/filebeat-logak.yml`. Behar duena:

    - `filestream` sarrera, identifikatzaile propioarekin, `/var/log/nginx/access.log` fitxategia irakurtzen.
    - `output.logstash`, `localhost:5044` helbidera. Ez gehitu `output.elasticsearch`.

**Eskema (lagungarria)** `filebeat-logak.yml` fitxategiarentzat (`filebeat-logak.esqueleto.yml`):

    # C BIDEA: ESKEMA (bigarren Filebeat). Bete ??? hutsuneak. Fitxategia: /etc/filebeat/filebeat-logak.yml
    filebeat.inputs:
      - type: ???
        id: web-sarbide-logak
        paths:
          - ???

    output.???:
      hosts: ["???"]

4.  **Logstash-en pipeline berria idatzi:** `/etc/logstash/conf.d/web-logak.conf`. Behar duena:

    - `beats` sarrera, 5044 portuan.
    - json iragazkia, message eremuko JSON testua eremu independente bihurtzen duena (nginx-ek jada JSON idazten duenez, ez da grok-ik behar).
    - date iragazkia, ordua eremutik @timestamp eguneratzeko. Pista: ordua ISO 8601 formatuan dator.
    - Garbiketa: ordua eta message eremuak kendu parseatu ondoren, baina soilik json iragazkiak ondo funtzionatu badu (\_jsonparsefailure etiketarik ez badago).
    - Irteera: `elasticsearch` (B bideko ezarpen berdinak), `web-logak-%{+YYYY.MM.dd}` indizera.

**Eskema (lagungarria)** `web-logak.conf` fitxategiarentzat (`web-logak.esqueleto.conf`):

    # C BIDEA: ESKEMA (Logstash pipeline). Bete ??? hutsuneak. Fitxategia: /etc/logstash/conf.d/web-logak.conf
    input {
      ??? { port => ??? }
    }

    filter {
      # Nginx-ek JSON idazten du: ez da grok-ik behar
      json { source => "???" }

      if "???" not in [tags] {
        date {
          match  => ["???", "???"]
          target => "???"
        }
        mutate { remove_field => ["???", "???"] }
      }
    }

    output {
      elasticsearch {
        hosts => ["https://localhost:9200"]
        user => "elastic"
        password => "${ES_PASSWORD}"
        ssl_enabled => true
        ssl_certificate_authorities => ["???"]
        index => "???"
        data_stream => "false"
      }
    }

5.  Sintaxia egiaztatu eta Logstash berrabiarazi:

- cd /usr/share/logstash
      sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash -f /etc/logstash/conf.d/web-logak.conf --config.test_and_exit
      sudo systemctl restart logstash

  Berrabiaraztean `sentsoreak-http` ere birkargatzen da. Egiaztatu B bidea ez dela hautsi.

6.  Filebeat-en bigarren instantzia abiarazi:

- sudo filebeat test config -c /etc/filebeat/filebeat-logak.yml -e
      sudo systemctl enable --now filebeat-logak
      sudo journalctl -u filebeat-logak -f

7.  Trafikoa sortu, egoera-kode desberdinekin:

- for i in $(seq 1 30); do
        curl -s -o /dev/null http://localhost/api/sentsoreak
        curl -s -o /dev/null http://localhost/osasuna
      done
      for i in $(seq 1 5); do curl -s -o /dev/null http://localhost/api/akatsa; done

**Egiaztapena:**

    GET web-logak-*/_search?size=3
    GET web-logak-*/_search
    { "size": 0, "aggs": { "egoerak": { "terms": { "field": "egoera_kodea" } } } }

**9. galdera:** zein egoera-kode agertzen dira eta zenbat aldiz? Zergatik dira `200` kodeak zuen eskuzko `curl` deiak baino askoz gehiago? Nork egiten ditu beste eskaerak? Zergatik daude orduak zuen lehen probetakoak ere (`@timestamp`)? (Pista: `filestream`-ek fitxategia hasieratik irakurtzen du lehen aldian.)

**10. galdera:** zergatik beharrezkoa da hemen bigarren Filebeat instantzia bat? Zer gertatuko litzateke `filebeat.yml` bakarrean bi irteera jarriz? Probatu: egin `/tmp/dos-salidas.yml` fitxategia bi irteerarekin eta exekutatu `sudo filebeat test config -c /tmp/dos-salidas.yml -e`.

**11. galdera:** Logstash gabe ere parseatu daitezke log-ak. Zein alternatiba ezagutzen duzue? (Pistak: Elasticsearch-eko *ingest pipeline*-ak, Filebeat-en moduluak.) Noiz da Logstash hobea? Gainera, nginx-ek JSON formatuan idazten du: zer abantaila eta zer muga ditu Apache “combined” formatuarekin alderatuta?

Hedapena (aukerazkoa, geoip): bidali eskaerak X-Forwarded-For goiburuarekin (curl -H "X-Forwarded-For: 8.8.8.8" http://localhost/osasuna) eta gehitu Logstash-en geoip iragazkia x_forwarded_for eremuarentzat, eremu hori hutsik ez dagoenean soilik. Zer eremu berri agertzen dira web-logak-\* indizean?

---
[← 5. fasea: B bidea, Logstash eta datuen garbiketa](05-fasea-B-logstash.md) | [Aurkibidea](index.md) | [7. fasea: D bidea, Heartbeat eta eskuragarritasuna →](07-fasea-D-heartbeat.md)
