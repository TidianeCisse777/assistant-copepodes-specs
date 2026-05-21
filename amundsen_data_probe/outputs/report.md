# Amundsen Science data probe

## 1. Datasets trouves
- Données CTD recueillies par le NGCC Amundsen dans l'Arctique canadien
  - id/name: `ca-cioos_ccin-12713`
  - license: Creative Commons Attribution 4.0
- Liste des stations scientifiques d'Amundsen — Journal des événements
  - id/name: `ca-cioos_ccin-13248`
  - license: Creative Commons Attribution 4.0
- Données de navigation (NAV) du NGCC Amundsen enregistrées lors des expéditions scientifiques annuelles dans l'Arctique canadien
  - id/name: `ca-cioos_ccin-12447`
  - license: Creative Commons Attribution 4.0

## 2. Acces et formats
- Données CTD recueillies par le NGCC Amundsen dans l'Arctique canadien: direct via ERDDAP, formats: ERDDAP
- Liste des stations scientifiques d'Amundsen — Journal des événements: on-demand / request form, formats: HTML
- Données de navigation (NAV) du NGCC Amundsen enregistrées lors des expéditions scientifiques annuelles dans l'Arctique canadien: direct via ERDDAP, formats: ERDDAP

## 3. Colonnes/variables detectees
- Données CTD recueillies par le NGCC Amundsen dans l'Arctique canadien / Jeu de données ERDDAP
  - `platform_name`
  - `platform_id`
  - `filename`
  - `cruise_name`
  - `cruise_number`
  - `cast_number`
  - `station`
  - `time (UTC)`
  - `latitude (degrees_north)`
  - `longitude (degrees_east)`
  - `PRES (decibars)`
  - `depth (m)`
  - `TE90 (degC)`
  - `PSAL (PSU)`
  - `OXYM (uM)`
  - `FLOR (ug/L)`
  - `NTRA (mmol/m^3)`

## 4. Cles de liaison disponibles
- cast_id: oui
- event_id: non
- station: oui
- date_time: oui
- lat/lon: oui
- depth: oui

## 5. Variables environnementales disponibles
- temperature: oui
- salinity/conductivity: oui
- oxygen: oui
- fluorescence: oui

## 6. Conclusion V1
- CTD-Rosette exploitable pour V1 ? oui
- Scientific Event Log exploitable ? a confirmer ; Amundsen l'indique comme on-demand pour 2003-2020.
- Navigation GPS exploitable ? utile seulement si les lat/lon des fichiers CTD/EcoPart ne suffisent pas.

## 7. Limites
- Probe volontairement limite a 3 datasets et 1 petit fichier par dataset.
- Si les ressources pointent vers ERDDAP, le pipeline final devra construire des URLs de sous-selection propres.
- Si une ressource est trop lourde, ce probe conserve seulement les metadonnees HTTP.
