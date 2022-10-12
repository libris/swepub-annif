See https://github.com/libris/swepub-redux/

## Install and run

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
# You might need to install dependencies, e.g. protobuf-compiler in Ubuntu
pip install -r requirements.txt
annif run -p 8084 # then check http://localhost:8084
# Or: gunicorn --workers 4 --threads 4 --worker-class gthread --bind 127.0.0.1:8084 "annif:create_app()"
```

## Create/update model

First, generate corpora. In swepub-redux repo with the swepub-redux venv:

```bash
source ./venv/bin/activate
# For quick testing, replace 0 with something low (e.g. 10000).
# 0 = get an unlimited amount of records.
bash misc/create_tsv_sets.sh en 0 3 5 ~/annif-input
bash misc/create_tsv_sets.sh sv 0 3 5 ~/annif-input
cd ~/annif-input
tail -n 800000 training_and_validation_en.tsv | gzip > swepub_en.tsv.gz
tail -n 800000 training_and_validation_sv.tsv | gzip > swepub_sv.tsv.gz
```

In _this_ repo and its own venv, train Annif:

```bash
source ./venv/bin/activate
annif load-vocab uka uka_terms.ttl
annif train -j 0 swepub-en ~/annif-input/training_en.tsv.gz # multiple (and non-gz) files also OK
annif train -j 0 swepub-sv ~/annif-input/training_sv.tsv.gz
```

Training `swepub-en` can take more than an hour if your SQLite database contains
the entirety of Swepub.

Note that the `omikuji-train.txt` files are not necessary for running the API
(especially the English one gets quite large) and should NOT be committed to the repo.

## (Re)generate uka_terms.ttl
`uka_terms.csv` was created from the Excel version of "Standard för svensk indelning av forskningsämnen 2011 (uppdaterad augusto 2016")
found [here](https://www.uka.se/statistik--analys/information-om-statistiken/amneslistor-och-huvudomraden/2017-02-14-forskningsamnen.html).

`uka_terms.ttl` is generated with:

```bash
python3 uka_terms_to_skos_ttl.py uka_terms.csv > uka_terms.ttl
````
