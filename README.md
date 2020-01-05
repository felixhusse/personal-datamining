# Personal Data Mining
Private projects to mine personal data mainly using python, elastic & kibana. My goal is to do some mining on the following datasets:
* mail
* netflix
* deutsche bahn

## Netflix View History
Scripts in subfolder "netflix" allow to extract your [viewing history](https://www.netflix.com/viewingactivity) on Netflix as JSON. A second functions 
allows to save this JSON to elasticsearch.

My plan was to answer the following questions:
* how long did I watch in the last year in total
* when do peaks of binge-watching appear
* how do I consume series on netflix (on-block vs. constantly)
* what type/genre do I prefer on netflix

### How to use
* add netflixId cookie content to config.json
* import Kibana Config (*.ndjson)
* run script.

### Technical background
This script uses the "shakti"-API, which is an undocumented API of netflix. It is mainly inspired by DDanielH repo https://github.com/DDanielH/netflix-personal-statistics. More details on the "shakti"-API can be found https://github.com/HowardStark/shakti.
