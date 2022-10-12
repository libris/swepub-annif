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

## Update model

First, generate corpora. In swepub-redux repo with the swepub-redux venv:

```bash
source ./venv/bin/activate
bash misc/create_tsv_sets.sh en 0 3 5 ~/annif-input
bash misc/create_tsv_sets.sh sv 0 3 5 ~/annif-input
cd ~/annif-input
tail -n 800000 training_and_validation_en.tsv | gzip > swepub_en.tsv.gz
tail -n 800000 training_and_validation_en.tsv | gzip > swepub_sv.tsv.gz
```

In _this_ repo and its own venv:

```bash
source ./venv/bin/activate
annif load-vocab uka uka_terms.ttl
annif train -j 0 swepub-en ~/annif-input/training_en.tsv.gz
annif train -j 0 swepub-sv ~/annif-input/training_en.tsv.gz
```
