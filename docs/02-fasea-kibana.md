[← 1. fasea: Elasticsearch](01-fasea-elasticsearch.md) | [Aurkibidea](index.md) | [3. fasea: web simulatua →](03-fasea-web.md)

# 2. fasea: Kibana

Kibana Elasticsearch-ekin lotzeko enrolamendu-token bat erabiltzen da. Tokenak 30 minutu ditu iraungitzeko, beraz sortu eta berehala erabili.

1.  Instalatu (oraindik ez abiarazi):

- sudo apt install -y kibana

2.  Tokena sortu eta Kibana-ri eman, komando bakar batean (tokenak 30 minutu ditu iraungitzeko, eta horrela ez duzue eskuz kopiatu behar; `TOKENA_HEMEN` literala kopiatzen baduzue `Invalid enrollment token` errorea ematen du):

- sudo /usr/share/kibana/bin/kibana-setup --enrollment-token "$(sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana)"

3.  Aukerazkoa: beste ekipo batetik Kibana-ra sartu nahi baduzue (ordenagailu beretik `http://localhost:5601` nahikoa da), editatu `/etc/kibana/kibana.yml` fitxategia eta aldatu lerro hau:

- server.host: "0.0.0.0"

4.  Abiarazi:

- sudo systemctl enable --now kibana

5.  Suebakia (`ufw`) aktibo badago, 5601 portua ireki:

- sudo ufw allow 5601/tcp

Kibana-k minutu bat behar du abiarazteko. Aurrerapena ikusteko: `sudo journalctl -u kibana -f` (irteteko, `Ctrl+C`). Fleet-i buruzko `WARN` mezuak (`encryptedSavedObjects`) normalak dira: Elastic Agent ez dugu erabiltzen.

**Egiaztapena:** nabigatzailean ireki `http://localhost:5601` (edo `http://MAKINAREN_IP:5601`, kanpotik sartzen bazarete), eta saioa hasi `elastic` erabiltzailearekin. Gero joan **Management \> Dev Tools** atalera eta exekutatu:

    GET /
    GET _cat/indices?v

Bi kontsultek erantzuna eman behar dute. Egin pantaila-argazki bat entregarako.

---
[← 1. fasea: Elasticsearch](01-fasea-elasticsearch.md) | [Aurkibidea](index.md) | [3. fasea: web simulatua →](03-fasea-web.md)
