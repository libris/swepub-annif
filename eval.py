# Quick and dirty script to compare stuff and generate plots,
# adjust as necessary to make it work.

import subprocess
from pathlib import Path
from datetime import datetime
import json
import sys

from pathvalidate import sanitize_filename
import matplotlib.pyplot as plt
import pandas as pd

PROJECTS_TO_TEST = [
    #"tfidf-en",
    "omikuji-parabel-en",
    #"omikuji-bonsai-en",
    #"fasttext-en-adv",
    #"ensemble-en",
]
METRICS_TO_DISPLAY = ["F1_score_doc_avg", "Precision_doc_avg", "Recall_doc_avg", "NDCG", "NDCG@5", "Precision@1", "Precision@5"]

EVAL_PARAMS = [
    #"--limit 2 --threshold 0.2",
    "--limit 5 --threshold 0.2",
]

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <training-file> <validation-file>")
    sys.exit(1)

training_file = sys.argv[1]
validation_file = sys.argv[2]

Path("./results").mkdir(parents=True, exist_ok=True)

results = {}

date_str = datetime.now().strftime("%Y%m%d_%H_%M_%S")
for project in PROJECTS_TO_TEST:
    subprocess.run(["annif", "train", "-j", "0", project, training_file])
    for eval_param in EVAL_PARAMS:
        metrics_filename = f"./results/metrics_{project}_{eval_param.replace(' ', '')}_{date_str}.json"

        eval_cmd = f"annif eval --metrics-file {metrics_filename} -j 0 {eval_param} {project} {validation_file}"
        subprocess.run(eval_cmd.split())

        with open(metrics_filename, "r") as json_file:
            results_dict = json.load(json_file)
            label = f"{project} {eval_param}"
            results[label] = {k: results_dict[k] for k in METRICS_TO_DISPLAY}

ax = pd.DataFrame(results).T.plot(ylim=(0,1), kind="bar", rot=-10, title=f"Train: {training_file}, validate/test: {validation_file}")
for container in ax.containers:
    ax.bar_label(container)

results_png_filename = f"./results/metrics_{date_str}.png"

plt.gcf().set_size_inches(14, 10)
plt.savefig(results_png_filename, dpi=100)
print(f"Saved plot to {results_png_filename}")
plt.show()
