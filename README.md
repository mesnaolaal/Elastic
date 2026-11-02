# Elastic Stack laborategi gidatua: sentsoreen datuak

Sistemak Big Data (5074) modulua. Elastic Stack 9.x **hutsetik** instalatuko duzue (`apt`, Dockerrik gabe) Ubuntu edo Linux Mint sisteman, eta sentsore simulatuen datuak lau bidetatik sartuko dituzue Elasticsearch-en:

| Bidea | Ibilbidea |
|---|---|
| A | Filebeat `httpjson` → Elasticsearch |
| B | Logstash `http_poller` + garbiketa → Elasticsearch |
| C | nginx log-ak → Filebeat `filestream` → Logstash → Elasticsearch |
| D | Heartbeat (eskuragarritasuna) |

Bukaeran, Kibana dashboard bat izango duzue bideak alderatzeko.

## Nola erabili

1. Egin repo honen **fork** bat (edo klonatu: `git clone URL_HEMEN`).
2. Jarraitu fasez fase, hurrenkeran. Fase bakoitzaren amaieran egiaztapen-scripta exekutatu dezakezue.
3. Bete `eskemak/` karpetako `???` hutsuneak (konfigurazioen eskemak). Irtenbideak ez daude hemen.
4. Galderak (`Q1`...`Q15`) zuen koadernoan erantzun eta entregatu.

## Aurkibidea

1. [Sarrera eta helburuak](docs/00-sarrera.md)
2. [0. fasea: sistema prestatu eta Elastic biltegia](docs/00-fasea-sistema.md)
3. [1. fasea: Elasticsearch](docs/01-fasea-elasticsearch.md)
4. [2. fasea: Kibana](docs/02-fasea-kibana.md)
5. [3. fasea: web simulatua](docs/03-fasea-web.md)
6. [4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era](docs/04-fasea-A-filebeat.md)
7. [5. fasea: B bidea, Logstash eta datuen garbiketa](docs/05-fasea-B-logstash.md)
8. [6. fasea: C bidea, Filebeat → Logstash (json) → Elasticsearch](docs/06-fasea-C-filebeat-logstash.md)
9. [7. fasea: D bidea, Heartbeat eta eskuragarritasuna](docs/07-fasea-D-heartbeat.md)
10. [8. fasea: egiaztapena eta Kibana dashboard-a](docs/08-fasea-dashboard.md)
11. [Entrega eta ebaluazio-irizpideak](docs/09-entrega.md)
12. [Ohiko akatsak eta arazo-konponketa](docs/10-arazoak.md)

## Egiaztapenak

Fase bakoitzaren ondoren exekutatu:

```bash
export ELASTIC_PASSWORD='zure-pasahitza'
./egiaztapenak/egiaztatu.sh 1     # 1: ES, 2: Kibana, 3: web, 4: A bidea, 5: B bidea, 6: C bidea, 7: D bidea
```

Scriptak ez du irtenbiderik ematen: `[OK]` edo `[EZ]` bakarrik. `[EZ]` bada, begiratu [arazo-konponketa](docs/10-arazoak.md) atala.

## Karpetak

- `docs/`: gidaren faseak (Markdown; web gisa argitaratzen da, ikus beheko oharra)
- `fitxategiak/web/`: web simulatua (Flask), nginx eta systemd fitxategiak
- `eskemak/`: konfigurazio-eskemak, `???` hutsuneekin
- `egiaztapenak/`: egiaztapen-scriptak

## Beharrezkoa

Ubuntu 22.04+ edo Linux Mint, 4 GB RAM gutxienez (8 GB gomendatua), 15 GB libre, `sudo` baimena.

## Gida web gisa

Repo honek GitHub Pages bidez argitaratzen du gida (`.github/workflows/web.yml`). Aktibatzeko: **Settings > Pages > Source: GitHub Actions**. Helbidea: `https://ERABILTZAILEA.github.io/ERREPOSITORIOA/`.
