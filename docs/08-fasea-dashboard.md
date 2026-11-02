[← 7. fasea: D bidea, Heartbeat eta eskuragarritasuna](07-fasea-D-heartbeat.md) | [Aurkibidea](index.md) | [Entrega eta ebaluazio-irizpideak →](09-entrega.md)

# 8. fasea: egiaztapena eta Kibana dashboard-a

Azken fasean lau bideen datuak batera ikusiko dituzue. Dashboard-ak argi utzi behar du A eta B bideen arteko aldea.

1.  Begiratu zein indize daukazuen eta zenbat dokumentu duten:

- GET _cat/indices?v&s=index

  Lau familia ikusi behar dituzue: `sentsoreak-beats`, `sentsoreak-logstash` (eta `sentsoreak-baztertuak`), `web-logak-*` eta `heartbeat-*`.

2.  **Stack Management \> Data Views** atalean, sortu data view bat indize-familia bakoitzarentzat (`@timestamp` ordu-eremu gisa): `sentsoreak-beats`, `sentsoreak-logstash`, `sentsoreak-baztertuak`, `web-logak-*` eta `heartbeat-*`.

3.  Begiratu **Discover** atalean `sentsoreak-beats` eta `sentsoreak-logstash` data view-ak, eta konparatu eremu-zerrendak (ikonoak ere: zenbakia, testua, geo…).

4.  Sortu dashboard bat, **Sentsoreen alderaketa** izenarekin, **Lens** (eta mapa baterako **Maps**) erabiliz. Denbora-tartea: azken ordua (datuak duela ordu gehiago sartu badituzue, zabaldu tartea); eguneratze automatikoa: 10 segundo.

| Panela                                 | Data view                                  | Mota             | Neurria eta taldekatzea                                                                                               |
|----------------------------------------|--------------------------------------------|------------------|-----------------------------------------------------------------------------------------------------------------------|
| Dokumentuak denboran, bidearen arabera | `sentsoreak-beats` + `sentsoreak-logstash` | Line (bi geruza) | Count, `@timestamp`                                                                                                   |
| Batez besteko balioa                   | `sentsoreak-logstash`                      | Bar              | Average `balioa`; X ardatza `mota`, Breakdown `zona`; **Unstacked**                                                   |
| Tenperaturaren p50 eta p95             | `sentsoreak-logstash`                      | Bar              | Percentile 50 eta Percentile 95 `balioa` (bi metrika), iragazkia `mota: temperatura`, X ardatza `zona`; **Unstacked** |
| Sentsoreen kokapena                    | `sentsoreak-logstash`                      | Maps (documents) | `kokapena`                                                                                                            |
| Baztertutako irakurketak               | `sentsoreak-baztertuak`                    | Metric           | Count                                                                                                                 |
| Eskaerak egoera-kodearen arabera       | `web-logak-*`                              | Bar              | Count, taldekatzea `egoera_kodea`                                                                                     |
| Zerbitzuaren egoera                    | `heartbeat-*`                              | Line             | Count; X ardatza `@timestamp`, Breakdown `monitor.status`                                                             |
| Erantzun-denbora                       | `heartbeat-*`                              | Line             | X ardatza `@timestamp`; Average eta Percentile 95 `monitor.duration.us`                                               |

5.  Gorde dashboard-a eta egin pantaila-argazki bat entregarako.

**Oharrak:** (1) Lens-en `Stacked` moduak metrikak batu egiten ditu (p50 + p95 ez da balio erreala): erabili `Unstacked`. (2) Panel bat hutsik ageri bada, begiratu bilatzailearen azpiko iragazki aktiboak (adib. `agent.type: filebeat`, grafikoan klik eginda sortzen da) eta kendu. (3) `web-logak-*` indizean testu-eremuak `.keyword` bidez taldekatzen dira (txantiloirik gabe sortu zelako). (4) Discover-ek `this.requests.values().filter is not a function` errorea ematen badu, nabigatzailea zaharra izan daiteke: eguneratu edo probatu beste batekin.

**14. galdera:** idatzi Dev Tools-en **tenperaturaren p50 eta p95 zonaka** kalkulatzen duen kontsulta (`sentsoreak-logstash` indizean, azken ordukoa). Ezin da dokumenturik itzuli: soilik agregazioak. Egiaztatu emaitza dashboard-eko panelarekin bat datorrela. Kontsulta Kibana-ren Dev Tools-en exekutatu, ez terminalean.

**15. galdera:** zergatik da p95 batezbestekoa baino informatiboagoa sentsore baten balio anomaloak detektatzeko? Zein arrisku du `-999` bezalako balio batek batezbestekoan, eta nola saihesten du B bideak?

**Hedapena (aukerazkoa):** sortu Kibana-n arau bat (*Alerting*) `monitor.status: down` duten dokumentuak hautematen dituena.

---
[← 7. fasea: D bidea, Heartbeat eta eskuragarritasuna](07-fasea-D-heartbeat.md) | [Aurkibidea](index.md) | [Entrega eta ebaluazio-irizpideak →](09-entrega.md)
