#!/usr/bin/env bash
# Erabilera: ELASTIC_PASSWORD=... ./egiaztatu.sh <fasea 1-7>
CA=/etc/elastic-ca/http_ca.crt
ES=https://localhost:9200
R=0
ok() { echo "  [OK]   $1"; }
ko() { echo "  [EZ]   $1"; R=1; }
es() { curl -s --cacert "$CA" -u "elastic:${ELASTIC_PASSWORD}" "$ES/$1"; }
cnt() { es "$1/_count" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("count",0))' 2>/dev/null || echo 0; }
svc() { systemctl is-active --quiet "$1" && ok "$1 aktibo" || ko "$1 ez dago aktibo (sudo systemctl status $1)"; }
docs() {
  local n
  n=$(cnt "$1")
  [ "${n:-0}" -gt 0 ] 2>/dev/null && ok "$1: $n dokumentu" || ko "$1 hutsik edo ez da existitzen"
}

if [ -z "$1" ]; then echo "Erabilera: $0 <1-7>"; exit 2; fi
if [ "$1" != 3 ] && [ -z "$ELASTIC_PASSWORD" ]; then echo "Ezarri ELASTIC_PASSWORD aldagaia"; exit 2; fi

case "$1" in
1) echo "1. fasea: Elasticsearch"
   [ -r "$CA" ] && ok "CA ziurtagiria irakurgarria ($CA)" || ko "CA falta da edo ez da irakurgarria"
   es "_cluster/health" | grep -qE '"status":"(green|yellow)"' && ok "Cluster-a green/yellow" || ko "Elasticsearch ez dago prest";;
2) echo "2. fasea: Kibana"
   curl -s -u "elastic:${ELASTIC_PASSWORD}" localhost:5601/api/status | grep -q '"level":"available"' && ok "Kibana available" || ko "Kibana ez dago prest (minutu bat itxaron)";;
3) echo "3. fasea: web simulatua"
   svc web-sentsoreak
   curl -s localhost/api/sentsoreak | python3 -c 'import sys,json;json.load(sys.stdin)["sentsoreak"]' 2>/dev/null && ok "nginx -> Flask: JSON zuzena" || ko "/api/sentsoreak ez dator JSON zuzena (nginx?)";;
4) echo "4. fasea: A bidea"
   svc filebeat
   docs sentsoreak-beats;;
5) echo "5. fasea: B bidea"
   svc logstash
   docs sentsoreak-logstash
   es "sentsoreak-logstash/_mapping" | grep -q '"balioa":{"type":"float"' && ok "balioa: float" || ko "balioa ez da float";;
6) echo "6. fasea: C bidea"
   svc filebeat-logak
   docs 'web-logak-*';;
7) echo "7. fasea: D bidea"
   svc heartbeat-elastic
   docs 'heartbeat-*';;
*) echo "Erabilera: $0 <1-7>"; exit 2;;
esac
exit $R
