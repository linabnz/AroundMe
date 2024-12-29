source ./loader.conf

update=false
if [ ${overwrite} == "true" ]; then
  echo "Overwrite is set to true. So if the data already exists, it will be downloaded again."
  update=true
else
  echo "Overwrite is set to false. So if the data already exists, it will not be downloaded again."
fi

# Téléchargement des informations sur les rues
if [ -f "../data/street_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Streets already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata.paris.fr"
 curl -X 'GET' \
  'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/denominations-emprises-voies-actuelles/exports/csv?delimiter=%2C&list_separator=%2C&quote_all=false&with_bom=true' \
  -H 'accept: */*' -o ../data/street_data_raw.csv
fi

# Téléchargement des informations sur les parkings
if [ -f "../data/parking_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Parking data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata.paris.fr"
 curl 'https://static.data.gouv.fr/resources/base-nationale-des-lieux-de-stationnement/20240109-111856/base-nationale-des-lieux-de-stationnement-outil-de-consolidation-bnls-v2.csv' -o ../data/parking_data_raw.csv
fi


# Téléchargement des informations sur les toilettes
if [ -f "../data/toilets_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Toilets data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from data.gouv.fr"
 curl 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/sanisettesparis/exports/csv?use_labels=true' -o ../data/toilets_data_raw.csv
fi

# Téléchargement des informations sur les musées
if [ -f "../data/museum_data_raw.json" ] && [ "$update" = false ]; then
  echo "Museum data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata"
 curl 'https://carto2.apur.org/apur/rest/services/OPENDATA/LIEUX_CULTURELS/MapServer/0/query?outFields=*&where=1%3D1&f=geojson' -o ../data/museum_data_raw.json
fi

# Téléchargement des informations sur les sports
if [ -f "../data/sports_data_raw.json" ] && [ "$update" = false ]; then
  echo "sports data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata"
 curl 'https://carto2.apur.org/apur/rest/services/OPENDATA/EQUIPEMENT_PONCTUEL/MapServer/3/query?outFields=*&where=1%3D1&f=geojson' -o ../data/sports_data_raw.json
fi