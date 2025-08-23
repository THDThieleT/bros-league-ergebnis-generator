# Bros League Rennergebnis und WM Stand Generator

Dieses Python Skript nimmt sich die Rennergebnis XML Datei des letzten Rennens und erstellt darauf basierend das Rennerergebnis.png

## Verwendung
Neben installiertem Python ist PILLOW nötig
```
pip3 install pillow
```
Danach kann **main.py** ausgeführt werden

## Erweiterung
- Flaggen als 1920x1080 Bild speichern
- Teamlogos mit vorhandener psd abgleichen (Größe 1000 x 1000 , wird auf 50x50 skaliert)
- Fahrer können in der driver_config.csv hinzugefügt werden

## Config Datein
- Race_names.csv: Renntitel der Rennen die in der Grafik auftauchen sollen nach Kalender sortiert
- team_config,csv: Offizieller Teamname, die Fahrer und welche Flagge geladen werden soll. **ACHTUNG!!** muss mit dem Namen in der driver_config.csv übereinstimmen
- Driver_config.csv: Gibt Infos für jeden Fahrer an. Die Info Stammfahrer wird verwendet um dem Team die Punkte in der WM hinzuzuschreiben. Wenn Ersatzfahrer auf Stammfahrer wechseln muss hier noch eine Erweiterung eingebaut werden, welche sicherstellt dass die Team WM Punkte nur aus der aktiven Zeit kommen und nicht vom Ersatzfahrer