[← 8. fasea: egiaztapena eta Kibana dashboard-a](08-fasea-dashboard.md) | [Aurkibidea](index.md) | [Ohiko akatsak eta arazo-konponketa →](10-arazoak.md)

# Entrega eta ebaluazio-irizpideak

Entregatu dokumentu bakar bat (PDF) pantaila-argazkiekin, konfigurazio-fitxategiekin eta galderen erantzunekin. **Pasahitzak eta tokenak ezkutatu** pantaila-argazkietan eta konfigurazioetan.

| Atala       | Zer entregatu                                                                                                                      | Pisua |
|-------------|------------------------------------------------------------------------------------------------------------------------------------|-------|
| 0-3. faseak | `_cluster/health` eta `_cat/indices?v` pantaila-argazkiak; Kibana-ren saio-hasiera; web simulatuaren `curl` probak; 1. galdera     | 15 %  |
| A bidea     | `filebeat.yml` (pasahitzik gabe); `sentsoreak-beats` indizearen `_count` eta `_mapping`; 2.-5. galderak                            | 15 %  |
| B bidea     | `sentsoreak.conf`; indize-txantiloiaren kontsulta; `_count` hiru indizeetan; 6.-8. galderak                                        | 25 %  |
| C bidea     | `web-sentsoreak.conf (nginx), filebeat-logak.yml, web-logak.conf eta pipelines.yml`````; egoera-kodeen agregazioa; 9.-11. galderak | 15 %  |
| D bidea     | `heartbeat.yml`; erorketa-probaren `down` dokumentuak; 12.-13. galderak                                                            | 10 %  |
| Dashboard-a | Pantaila-argazkia, zortzi panelekin; 14.-15. galderak                                                                              | 10 %  |
| Gogoeta     | 250 hitz gehienez, behean azaldua                                                                                                  | 10 %  |

**Gogoeta.** Idatzi zein bide erabiliko zenukeen egoera hauetan, eta zergatik: (a) JSON garbia ematen duen API bat; (b) kalitate txarreko datuak dituen sentsore-sare bat; (c) zerbitzu baten log-ak; (d) zerbitzua erori dela jakin nahi duzue. Eman bide bakoitzaren abantaila eta muga bana.

**Irizpide-gida laburra:** B bidean batez ere garbiketa baloratuko da (hiru kasu bereiziak: zenbakia, testu zenbakizkoa eta balio baliogabea), mapaketa zuzena eta baztertuen indizea.

---
[← 8. fasea: egiaztapena eta Kibana dashboard-a](08-fasea-dashboard.md) | [Aurkibidea](index.md) | [Ohiko akatsak eta arazo-konponketa →](10-arazoak.md)
