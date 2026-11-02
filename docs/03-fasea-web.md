[← 2. fasea: Kibana](02-fasea-kibana.md) | [Aurkibidea](index.md) | [4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era →](04-fasea-A-filebeat.md)

# 3. fasea: web simulatua

Irakasleak `web_sentsoreak.py` fitxategia emango dizue. Flask aplikazio txiki bat da, sentsoreen irakurketak API REST bidez eskaintzen dituena eta 127.0.0.1:5000 helbidean soilik entzuten duena. Haren aurrean nginx jarriko duzue proxy inberso gisa (80 portua); nginx-ek idatziko du sarbide-log-a JSON formatuan. Zuen lana ez da kodea idaztea, martxan jartzea eta datuak aztertzea baizik.

| Endpoint          | Zer egiten du                      | Zein bidek erabiltzen du     |
|-------------------|------------------------------------|------------------------------|
| `/api/sentsoreak` | 9 sentsoreren irakurketak JSON-ean | A eta B                      |
| `/osasuna`        | Tarteka `503` itzultzen du         | D                            |
| `/api/akatsa`     | Beti `500` itzultzen du            | C (logetan akatsak sortzeko) |

1.  Karpeta eta ingurune birtuala prestatu:

- mkdir -p ~/web && cd ~/web
      python3 -m venv venv
      ./venv/bin/pip install flask

2.  Kopiatu `web_sentsoreak.py` fitxategia `~/web` karpetara eta egiaztatu hor dagoela (bestela hurrengo urratseko zerbitzuak `status=2` errorearekin huts egingo du):

<!-- -->

    ls ~/web

3.  Zerbitzu gisa konfiguratu, makina berrabiaraztean ere martxan egon dadin:

- sudo tee /etc/systemd/system/web-sentsoreak.service > /dev/null <<EOF
      [Unit]
      Description=Web simulatua (sentsoreak)
      After=network.target

      [Service]
      User=$USER
      WorkingDirectory=/home/$USER/web
      ExecStart=/home/$USER/web/venv/bin/python web_sentsoreak.py
      Restart=on-failure

      [Install]
      WantedBy=multi-user.target
      EOF

      sudo systemctl daemon-reload
      sudo systemctl enable --now web-sentsoreak

4.  Nginx instalatu. Flask-en aurrean proxy inberso gisa jarriko da (80 portua), eta sarbide-log-a JSON formatuan idatziko du. Nginx lehenetsitako gune-fitxategia kendu behar da, 80 portua okupatzen baitu:

- sudo apt install -y nginx
      sudo rm -f /etc/nginx/sites-enabled/default

5.  Idatzi nginx-en konfigurazioa (nginx konfiguratzea ez da praktikaren helburua, beraz fitxategia emana da). Lerro bakoitzak JSON objektu bat idatziko du log-ean, eremu-izen euskaldunekin:

- sudo tee /etc/nginx/conf.d/web-sentsoreak.conf > /dev/null <<'EOF'
      # Sarbide-log-a JSON formatuan idazten du (lerro bakoitza JSON objektu bat da).
      log_format json_logak escape=json
        '{'
          '"ordua":"$time_iso8601",'
          '"bezeroa":"$remote_addr",'
          '"x_forwarded_for":"$http_x_forwarded_for",'
          '"metodoa":"$request_method",'
          '"url":"$request_uri",'
          '"egoera_kodea":$status,'
          '"byteak":$body_bytes_sent,'
          '"erreferentzia":"$http_referer",'
          '"user_agent":"$http_user_agent",'
          '"erantzun_denbora":$request_time'
        '}';

      server {
          listen 80;
          server_name _;

          access_log /var/log/nginx/access.log json_logak;

          location / {
              proxy_pass http://127.0.0.1:5000;
              proxy_set_header Host $host;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          }
      }
      EOF

6.  Sintaxia egiaztatu eta nginx abiarazi:

- sudo nginx -t
      sudo systemctl enable nginx
      sudo systemctl restart nginx

7.  Probatu (nginx bidez, 80 portua) eta log-ak sortu:

- curl -s http://localhost/api/sentsoreak | jq
      for i in $(seq 1 5); do curl -s http://localhost/osasuna; done
      curl -s http://localhost/api/akatsa
      sudo tail -n 5 /var/log/nginx/access.log

**Egiaztapena:** lehen komandoak `sentsoreak` zerrenda bat itzuli behar du, eta /var/log/nginx/access.log fitxategiak JSON lerro berriak izan behar ditu (egoera_kodea, url, erantzun_denbora… eremuekin).``

**Datu zikinak.** Irakurketen %15 inguru nahita “zikina” da. Exekutatu `curl` hori hainbat aldiz eta idatzi zein motatako zikinkeria ikusten duzuen `balioa` eremuan. Bide bakoitzean zer gertatzen den alderatzeko behar dituzue: Zikinkeria bakarrik ikusteko: `for i in $(seq 1 20); do curl -s http://localhost/api/sentsoreak; done | jq -M -c '.sentsoreak[] | select((.balioa|type)!="number" or .balioa == -999) | {sentsore_id, balioa}'` (`-M`: koloreak kentzeko; bestela `null` ez da ikusten).

- zenbakia testu gisa (`"16.1"`),
- `null`,
- balio ezinezkoa (`-999`),
- testu ez-zenbakizkoa (`"N/A"`).

**1. galdera:** zer arazo sortuko lituzke `"N/A"` balio bat `float` motako eremu batean gordetzeak Elasticsearch-en?

---
[← 2. fasea: Kibana](02-fasea-kibana.md) | [Aurkibidea](index.md) | [4. fasea: A bidea, Filebeat zuzenean Elasticsearch-era →](04-fasea-A-filebeat.md)
