To use with https://github.com/libris/swepub-redux/

See https://github.com/NatLibFi/Annif for general Annif instructions and advice.

## Install and run

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 -m nltk.downloader punkt
annif run -p 8084 # then check http://localhost:8084
# Instead of `annif run` (for development only), you could use gunicorn, e.g.:
# gunicorn --workers 4 --threads 4 --worker-class gthread --bind 127.0.0.1:8084 "annif:create_app()"
# (...and put behind e.g. nginx in a production environment)
```

(For `pip install` to work you might need to install some dependencies, e.g. `protobuf-compiler` in Ubuntu.)

Visit http://localhost:8084 to try the Annif UI. You'll also find Swagger there.

You can also test Annif from the command line, e.g.:

```bash
echo 'Cardiac troponin I in healthy Norwegian Forest Cat, Birman and domestic shorthair cats, and in cats with hypertrophic cardiomyopathy' | annif suggest swepub-en
2022-10-11T13:10:35.736Z INFO [omikuji::model] Loading model from data/projects/swepub-en/omikuji-model...
...
<https://id.kb.se/term/uka/4> Agricultural and Veterinary sciences  0.8900570869445801
<https://id.kb.se/term/uka/40303> Clinical Science  0.6352069973945618
<https://id.kb.se/term/uka/403> Veterinary Science  0.4740253984928131
<https://id.kb.se/term/uka/106> Biological Sciences (Medical to be 3 and Agricultural to be 4) 0.17030012607574463
...
```

(This will be slow as the model has to be loaded each time you use `suggest`; normally you should use the REST API.)

## Update model

NOTE: this repo already contains a pre-trained model. The following is only if you want to update it (i.e., recreate
it from scatch).

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
