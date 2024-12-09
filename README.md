To use with https://github.com/libris/swepub-redux/

See https://github.com/NatLibFi/Annif for general Annif instructions and advice.

## Install and run

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
annif run -p 8083 # then check http://localhost:8083
# Instead of `annif run` (for development only), you could use gunicorn, e.g.:
# gunicorn --workers 4 --threads 4 --worker-class gthread --bind 127.0.0.1:8083 "annif:create_app()"
# (...and put behind e.g. nginx in a production environment)
```

(For `pip install` to work you might need to install some dependencies, e.g. `protobuf-compiler` in Ubuntu.)

Visit http://localhost:8083 to try the Annif UI. You'll also find Swagger there.

You can also test Annif from the command line, e.g.:

```bash
echo 'Cardiac troponin I in healthy Norwegian Forest Cat, Birman and domestic shorthair cats, and in cats with hypertrophic cardiomyopathy' | annif suggest swepub-en
2022-10-11T13:10:35.736Z INFO [omikuji::model] Loading model from data/projects/swepub-en/omikuji-model...
...
<https://id.kb.se/term/ssif/4> Agricultural and Veterinary sciences  0.8900570869445801
<https://id.kb.se/term/ssif/40303> Clinical Science  0.6352069973945618
<https://id.kb.se/term/ssif/403> Veterinary Science  0.4740253984928131
<https://id.kb.se/term/ssif/106> Biological Sciences (Medical to be 3 and Agricultural to be 4) 0.17030012607574463
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
tail -n 800000 training_en.tsv | gzip > training_en.tsv.gz
tail -n 800000 training_sv.tsv | gzip > training_sv.tsv.gz
```

In _this_ repo and its own venv, train Annif:

```bash
source ./venv/bin/activate
annif load-vocab ssif ssif_terms.ttl
annif train -j 0 swepub-en ~/annif-input/training_en.tsv.gz # multiple (and non-gz) files also OK
annif train -j 0 swepub-sv ~/annif-input/training_sv.tsv.gz
```

Training `swepub-en` can take more than an hour if your SQLite database contains
the entirety of Swepub.

Note that the `omikuji-train.txt` files are not necessary for running the API
(especially the English one gets quite large) and should NOT be committed to the repo.

Additionally, for practical reasons, we _do_ like to keep the latest models in this Git repo without having to use
Git LFS or similar, so as to not exceed GitHub limits we use [BFG Repo Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)
to remove large files from history after updating the models (i.e. we forcibly rewrite the Git history):

```
java -jar ~/somewhere/bfg-1.14.0.jar --delete-files '{*.cbor,vectorizer}'
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

## (Re)generate ssif_terms.ttl
`ssif_terms.csv` was created from the Excel version of "Standard för svensk indelning av forskningsämnen 2011 (uppdaterad augusti 2016)"
found [here](https://web.archive.org/web/20230201060649/https://www.uka.se/statistik--analys/information-om-statistiken/amneslistor-och-huvudomraden/2017-02-14-forskningsamnen.html).

`ssif_terms.ttl` is generated with:

```bash
python3 ssif_terms_to_skos_ttl.py ssif_terms.csv > ssif_terms.ttl
````
