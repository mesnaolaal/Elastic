[Aurkibidea](index.md) | [0. fasea: sistema prestatu eta Elastic biltegia →](00-fasea-sistema.md)

# Sarrera eta helburuak

Praktika honetan Elastic Stack-a hutsetik instalatuko duzue Ubuntu (edo Linux Mint) sistema batean, eta sentsoreen datuak lau bidetatik sartuko dituzue Elasticsearch-en. Helburua da ikustea noiz nahikoa den Beats eta noiz behar den Logstash.

**Eszenatokia.** Hiri bateko sentsore-sare simulatu bat dago (tenperatura, hezetasuna, CO₂). Sentsoreen irakurketak web simulatu batek eskaintzen ditu API REST baten bidez. Zuek datu horiek jaso, prozesatu, gorde eta Kibana-n erakutsi behar dituzue.

**Praktika honen bukaeran gai izango zarete:**

- Elasticsearch, Kibana, Logstash, Filebeat eta Heartbeat bertsio berean instalatu eta konfiguratzeko.
- Beats-ek zuzenean eta Logstash-ek iragazkiekin egiten dutenaren aldea azaltzeko.
- Datu zikinak (testu bihurtutako zenbakiak, nuluak, balio ezinezkoak) detektatu eta garbitzeko.
- Mapaketa egokia (keyword, float, date, geo_point) aukeratzeko.
- Kibana-n dashboard bat eraikitzeko, bi indizeak alderatuz.

**Aurrekoak:** Linux oinarriak (terminala, `sudo`, `systemctl`), JSON eta HTTP oinarriak, eta 05–08 aurkezpenetako Elastic Stack kontzeptuak.

### Lau ingesta-bideak

| Bidea | Ibilbidea                                                   | Zer ikasten da                                                          | Indizea               |
|-------|-------------------------------------------------------------|-------------------------------------------------------------------------|-----------------------|
| A     | Filebeat (`httpjson`) → Elasticsearch                       | Beats nahikoa denean: datuak JSON garbian datozenean                    | `sentsoreak-beats`    |
| B     | Logstash (`http_poller` + iragazkiak) → Elasticsearch       | Datuak eraldatzea: motak, izenak, baztertzea, aberastea                 | `sentsoreak-logstash` |
| C     | Filebeat (filestream) → Logstash (json) → Elasticsearch```` | Ekoizpeneko eredu ohikoena: Beats bidaltzen du, Logstash prozesatzen du | `web-logak-*`         |
| D     | Heartbeat → Elasticsearch                                   | Zerbitzuaren eskuragarritasuna (uptime) monitorizatzea                  | `heartbeat-*`         |

**Zikinkeria nahita.** Web simulatuak datu batzuk nahita “zikinak” itzultzen ditu. A bideak datu horiek bere horretan gordeko ditu; B bideak garbituko ditu. Praktikaren ondorioa alde hori ikustea da.

---
[Aurkibidea](index.md) | [0. fasea: sistema prestatu eta Elastic biltegia →](00-fasea-sistema.md)
