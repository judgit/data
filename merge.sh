#!/bin/sh
d=`date +%F`
mkdir -p dest/$d
# echo write rdf
# python3 to_rdf.py > dest/$d/judgit.$d.rdf
echo write ndjson
python3 to_ndjson.py > dest/$d/judgit.$d.ndjson
echo write ndjson for bq
python3 to_bigquery.py > dest/$d/judgit.$d.bq.ndjson
# echo write json
# python3 to_json.py > dest/$d/judgit.$d.json
