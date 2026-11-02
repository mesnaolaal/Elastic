[← 4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era](04-fasea-A-filebeat.md) | [Aurkibidea](index.md) | [6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch →](06-fasea-C-filebeat-logstash.md)

# 5. fasea: B bidea, Logstash eta datuen garbiketa

Helburua: Logstash-ek API-a kontsultatu, irakurketak banandu, datu zikinak detektatu eta garbitu, eta emaitza `sentsoreak-logstash` indizean gordetzea. Datu baliogabeak ez dira galduko: `sentsoreak-baztertuak` indizera joango dira.

1.  Logstash instalatu:

- sudo apt install -y logstash

2.  Pasahitza Logstash-en keystore-an gorde. `.deb` instalazioan keystore-a `sudo` bidez sortzen da (ez `-u logstash` erabiliz), eta gero `logstash` erabiltzaileak irakurri ahal izateko jabetza aldatzen da. Pasahitzik gabeko keystore bat sortzeko baimena eskatzen badu, `y` erantzun (ikasgela da):

- cd /usr/share/logstash
      sudo /usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash create
      sudo /usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash add ES_PASSWORD
      sudo chown logstash:root /etc/logstash/logstash.keystore
      sudo chmod 0600 /etc/logstash/logstash.keystore
      sudo -u logstash /usr/share/logstash/bin/logstash-keystore --path.settings /etc/logstash list

**Oharra:** `sudo -u logstash` erabiltzen duten komandoak `/usr/share/logstash` karpetatik exekutatu behar dira; bestela `No such file or directory - /home/ZURE_ERABILTZAILEA/...` errorea ematen dute, `logstash` erabiltzaileak zuen karpeta pertsonala irakurri ezin duelako. `list`-ek `es_password` erakusten du minuskulaz; `${ES_PASSWORD}` erabiltzen jarraitu dezakezue.

3.  **Indize-txantiloia sortu Kibana Dev Tools-en.** Logstash-en indizeak mapaketa zuzenarekin sortu behar dira, bestela Elasticsearch-ek lehen dokumentuaren arabera asmatuko du (A bidean gertatu zen bezala). Idatzi `PUT _index_template/sentsoreak-logstash` kontsulta, `sentsoreak-logstash*` ereduarentzat eta ondorengo mapaketarekin:

| Eremua                                             | Mota        |
|----------------------------------------------------|-------------|
| `sentsore_id`, `mota`, `unitatea`, `zona`, `bidea` | `keyword`   |
| `balioa`                                           | `float`     |
| `kokapena`                                         | `geo_point` |
| `@timestamp`                                       | `date`      |

4.  **Pipeline-a idatzi:** `/etc/logstash/conf.d/sentsoreak.conf`.

**Pipeline-ak egin behar duena:**

- `http_poller` sarrera, `http://localhost/api/sentsoreak` helbidera, 10 segundoz behin, JSON kodekarekin. Erantzun osoa ebento bakarra da.
- Erantzuna JSON baliozkoa ez bada (adibidez web-a erori denean: nginx-ek `502 Bad Gateway` HTML orria itzultzen du), ebentoak `_jsonparsefailure` etiketa izango du. Ebento hori `drop` bidez baztertu, `split` baino lehen, `sentsoreak-baztertuak` indizea ez zikintzeko.
- `split` iragazkiarekin, `sentsoreak` zerrendako elementu bakoitza ebento independente bihurtu.
- Eremuak erro mailara eraman (`mutate` + `rename`) eta eremu laguntzaileak kendu (`sentsoreak`, `@version`, `http_poller_metadata`…).
- `denbora` eremuko ordua `@timestamp` bihurtu (`date` iragazkia, ISO8601).
- `bidea` izeneko eremu bat gehitu, `logstash` balioarekin.
- **Balioaren garbiketa:**
  1.  Jatorrizko balioa `balio_gordina` eremuan gorde, testu gisa.
  2.  Balioa baliozkoa bada (zenbakia, testu zenbakizkoa barne, eta `-999` ez dena): `float` bihurtu eta `[@metadata][indizea]` = `sentsoreak-logstash`.
  3.  Bestela: `balioa` kendu, `balio_baliogabea` etiketa jarri eta `[@metadata][indizea]` = `sentsoreak-baztertuak`.
- Irteera: `elasticsearch`, HTTPS bidez, CA ziurtagiriarekin (`/etc/elastic-ca/http_ca.crt`), `elastic` erabiltzailearekin, keystore-ko pasahitzarekin eta `index => "%{[@metadata][indizea]}"`.

Pistak: `mutate` bidez testu ez-zenbakizko bat `float` bihurtzea ez da fidagarria; egiaztatu lehenik adierazpen erregular batekin. Frogatu zuen kasuan nola portatzen den `"N/A"` baliorekin. `@metadata` barruko eremuak ez dira Elasticsearch-era bidaltzen.

**Eskema (lagungarria).** Bete `???` hutsuneak. `rename` blokea emanda dago. Fitxategi gisa ere badago (`sentsoreak.esqueleto.conf`).

    # B BIDEA: ESKEMA. Bete ??? hutsuneak. Fitxategia: /etc/logstash/conf.d/sentsoreak.conf
    input {
      http_poller {
        urls => {
          sentsoreak => "???"
        }
        schedule => { every => "???" }
        codec => "???"
        request_timeout => 10
      }
    }

    filter {
      # 0. Erantzuna JSON baliozkoa ez bada (adib. web-a erori da eta nginx-ek 502 HTML orria itzultzen du),
      #    ebentoa baztertu: ez dugu nahi sentsoreak-baztertuak indizea zikintzea
      if "???" in [tags] { drop {} }

      # 1. Zerrenda banatu: irakurketa bakoitza ebento bat da
      split { field => "???" }

      # 2. Eremuak erro mailara eraman eta bidea markatu
      mutate {
        rename => {
          "[sentsoreak][sentsore_id]" => "sentsore_id"
          "[sentsoreak][mota]"        => "mota"
          "[sentsoreak][balioa]"      => "balioa"
          "[sentsoreak][unitatea]"    => "unitatea"
          "[sentsoreak][zona]"        => "zona"
          "[sentsoreak][kokapena]"    => "kokapena"
          "[sentsoreak][denbora]"     => "denbora"
        }
        add_field => { "bidea" => "???" }
      }

      # 3. Sentsorearen ordua @timestamp bihurtu
      date {
        match => ["???", "???"]
        target => "???"
      }

      # 4. Balioaren garbiketa: lehenik testu bihurtu, jatorrizkoa gorde
      mutate { convert => { "balioa" => "???" } }
      mutate { copy => { "balioa" => "???" } }

      if [balioa] =~ /???/ and [balioa] != "???" {
        mutate {
          convert => { "balioa" => "???" }
          remove_field => ["???"]
          add_field => { "[@metadata][indizea]" => "???" }
        }
      } else {
        mutate {
          remove_field => ["???"]
          add_tag => ["???"]
          add_field => { "[@metadata][indizea]" => "???" }
        }
      }

      # 5. Eremu laguntzaileak kendu
      mutate { remove_field => ["???", "@version", "???", "event"] }
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

5.  Sintaxia egiaztatu (Logstash-en erabiltzailearekin, bestela fitxategien jabetza hautsiko duzue; `/usr/share/logstash` karpetatik):

- cd /usr/share/logstash
      sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash -f /etc/logstash/conf.d/sentsoreak.conf --config.test_and_exit

  Minutu bat tardatzen du. `Configuration OK` ikusi behar duzue. `UserMetric`, `ECS compatibility` eta `pipelines.yml` ez dela erabiltzen dioten abisuak normalak dira.

6.  Abiarazi. Logstash-ek 1-2 minutu behar ditu hasteko:

- sudo systemctl enable --now logstash
      sudo journalctl -u logstash -f

**Egiaztapena:**

    GET sentsoreak-logstash/_count
    GET sentsoreak-baztertuak/_count
    GET sentsoreak-baztertuak/_search?size=5
    GET sentsoreak-logstash/_mapping

**6. galdera:** zenbat dokumentu daude `sentsoreak-beats` eta `sentsoreak-logstash` indizeetan? Zergatik ez dute kopuru bera, bi bideek 10 segundoro irakurtzen badute?

**7. galdera:** zein balio daude `sentsoreak-baztertuak` indizean? Zergatik hobe da balio baliogabeak ezabatu beharrean beste indize batean gordetzea?

**8. galdera:** Filebeat-ek ere prozesadoreak ditu. Zergatik da Logstash egokiagoa garbiketa honetarako? Zein muga ikusi dituzue Filebeat-en prozesadoreekin?

---
[← 4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era](04-fasea-A-filebeat.md) | [Aurkibidea](index.md) | [6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch →](06-fasea-C-filebeat-logstash.md)
