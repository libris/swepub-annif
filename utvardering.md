### Autoklassningsjämförelse

För autoklassning använde Swepub tidigare (t o m version 1.8) en implementation av en enkel
variant av [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).

Från Swepub 1.9 använder vi nu [Omikuji](https://github.com/tomtung/omikuji), som är en implementation
av [Partitioned Label Trees](https://dl.acm.org/doi/10.1145/3178876.3185998) (Prabhu et al., 2018). Detta
sker via [Annif](https://annif.org/), ett fritt verktyg utvecklat av Nationalbiblioteket i Finland för just
automatisk ämnesklassificering. Annif fungerar som ett "frontend", eller gränssnitt, mot olika backends -- bl.a.
Omikuji och nämnda TF-IDF -- och gör det också enkelt att jämföra dem.

Efter att ha testat olika backends som Annif erbjöd märkte vi snabbt att Omikuji presterade bäst, och avsevärt
bättre än den tidigare lösningen. (Även fastText, utvecklat av Facebook Research, presterade bra -- men var betydligt
mer resurskrävande.)

Nedan följer en jämförelse mellan Omikuji (med språkspecifik modell) och en approximation av den tidigare lösningen
(som använde en och samma "modell" för både svenska och engelska). Båda modellerna tränades med
800 000 dokument. Enbart klassningar på 1- och 3-siffernivå togs med. 20 000 dokument testades, dvs: 20 000 dokument
som modellen inte sett tidigare, och som redan klassats av lärosätena, så att vi kan jämföra lärosätenas klassningar
med vad TF-IDF och Omikuji (via Annif) föreslår.

![TF-IDF vs Omikuji](metrics_20221020_18_31_55.png?raw=true "TF-IDF vs Omikuji]")

Skalan är från 0 till 1, där 1 är bäst. Gamla i staplarna till vänster, nya i staplarna till höger.

Orange:a stapeln, precision, svarar på frågan "hur många av de föreslagna klassningarna var faktiskt korrekta?".

Gröna stapeln, recall, svarar på frågan "hur många av klassningarna som borde föreslagits, föreslogs faktiskt?".

Som synes har den gamla autoklassningen till vänster hyfsat hög recall men väldigt låg precision, dvs den ger väldigt
många false positives (klassningar den inte borde gett).

Blåa stapeln, F1, är det harmoniska medelvärdet mellan precision och recall.

Här lämpar sig ett citat från Annif-dokumentationen, ["Achieving good results"](https://github.com/NatLibFi/Annif/wiki/Achieving-good-results):

> Be aware that subject indexing is a subjective task. It is very unlikely that two humans given the same document will come up with exactly the same subjects for it. According to many empirical studies, inter-indexer agreement tends to be somewhere in between 30% and 50%. It's unrealistic to expect that an algorithm can do much better than this - though it must be noted that the differences between humans are often more matters of perspective, whereas algorithms tend to make outright errors that a human would never make. It can be very informative to actually have several people assign subjects for the same set of documents and measure how similar or different they are. It will always surprise everyone involved. For some background on inter-indexer consistency and automated indexing, Alyona Medelyan's PhD thesis [Human-competitive automatic topic indexing](https://researchcommons.waikato.ac.nz/handle/10289/3513) is highly recommended reading.

(Här ska dock nämnas att mängden "SSIF-klassningar på 1- eller 3-siffernivå" endast är 48 ämnen.)

Visualiseringen ovan genererades utifrån följande JSON med statistik producerad av Annif:

TF-IDF:
```json
{
  "Precision_doc_avg": 0.21652083333333336,
  "Recall_doc_avg": 0.5005105988455988,
  "F1_score_doc_avg": 0.2954709951159951,
  "Precision_subj_avg": 0.0327206785382862,
  "Recall_subj_avg": 0.07786284094670463,
  "F1_score_subj_avg": 0.03772014234867286,
  "Precision_weighted_subj_avg": 0.4311350347072359,
  "Recall_weighted_subj_avg": 0.4838182266120182,
  "F1_score_weighted_subj_avg": 0.3995877119806384,
  "Precision_microavg": 0.23417563714809153,
  "Recall_microavg": 0.4838182266120182,
  "F1_score_microavg": 0.31559724170172976,
  "F1@5": 0.2954709951159951,
  "NDCG": 0.4186961500964299,
  "NDCG@5": 0.41923718892146816,
  "NDCG@10": 0.4186968258373717,
  "Precision@1": 0.35355,
  "Precision@3": 0.26374166666666665,
  "Precision@5": 0.21652083333333336,
  "LRAP": 0.3443752107383324,
  "True_positives": 21602,
  "False_positives": 70645,
  "False_negatives": 23047,
  "Documents_evaluated": 20000
}
```

Omikuji:
```json
{
  "Precision_doc_avg": 0.7662533333333332,
  "Recall_doc_avg": 0.7961145238095237,
  "F1_score_doc_avg": 0.7554614718614718,
  "Precision_subj_avg": 0.0966953926575131,
  "Recall_subj_avg": 0.07986208634680152,
  "F1_score_subj_avg": 0.08385113073618966,
  "Precision_weighted_subj_avg": 0.7229019344872509,
  "Recall_weighted_subj_avg": 0.7488490041115788,
  "F1_score_weighted_subj_avg": 0.7303498311001695,
  "Precision_microavg": 0.7310308361573774,
  "Recall_microavg": 0.7488490041115788,
  "F1_score_microavg": 0.739832652266978,
  "F1@5": 0.7554614718614718,
  "NDCG": 0.8023203110082616,
  "NDCG@5": 0.8028819671373697,
  "NDCG@10": 0.8023203110082616,
  "Precision@1": 0.8563,
  "Precision@3": 0.7694333333333333,
  "Precision@5": 0.7662533333333333,
  "LRAP": 0.7661337505411534,
  "True_positives": 30416,
  "False_positives": 11191,
  "False_negatives": 10201,
  "Documents_evaluated": 20000
}
```