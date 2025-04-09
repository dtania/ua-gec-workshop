# ua-gec-workshop
Data and code for the workshop held as a part of the ['Building LLM-Powered Features' Grammarly meetup](https://www.facebook.com/events/1008154811405353/).

## Contents
### Workshop Notebook

Tasks for the workshop can be found in [Ukrainian_GEC.ipynb](https://github.com/dtania/ua-gec-workshop/blob/main/Ukrainian_GEC.ipynb).

### Data

The data is extracted from [UNLP 2023 Shared Task data](https://github.com/unlp-workshop/unlp-2023-shared-task/tree/main/data/gec-only) for [GEC-only track](https://github.com/unlp-workshop/unlp-2023-shared-task/tree/main?tab=readme-ov-file#track-1-gec-only). The script for downloading and cleaning the data can be found [here](https://github.com/dtania/ua-gec-workshop/blob/main/utils/clean_data.py). Data files are stored in [data/dev](https://github.com/dtania/ua-gec-workshop/tree/main/data/dev) and [data/eval](https://github.com/dtania/ua-gec-workshop/tree/main/data/eval).

Each of these folders contains a similar set of files:

* `dev_src_data.txt` and `eval_src_data.txt` -- original (uncorrected) texts for development (60 sentences) and evaluation (200 sentences) of the solution. Commands that were used to extract these files are:
```bash
python clean_data.py --type txt --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/train.src.txt" --output "dev_src_data.txt" --num 60
```
and
```bash
python clean_data.py --type txt --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/valid.src.txt" --output "eval_src_data.txt"
```
* `dev_tgt_data.txt` and `eval_tgt_data.txt` -- corrected texts, untokenized versions:
```bash
python clean_data.py --type txt --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/train.tgt.txt" --output "dev_tgt_data.txt" --num 60
```
and
```bash
python clean_data.py --type txt --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/valid.tgt.txt" --output "eval_tgt_data.txt"
```
* `dev.m2` and `eval.m2` -- development and validation data annotated in the [M2 format](https://github.com/chrisjbryant/errant?tab=readme-ov-file#overview):

```bash
python clean_data.py --type m2 --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/train.m2" --output "dev.m2" --num 60
```
and
```bash
python clean_data.py --type m2 --url "https://raw.githubusercontent.com/unlp-workshop/unlp-2023-shared-task/main/data/gec-only/valid.m2" --output "eval.m2"
```

### Evaluation script

The evaluation script is cloned from the [unlp-2023-shared-task](https://github.com/unlp-workshop/unlp-2023-shared-task) repository and is stored [here](https://github.com/dtania/ua-gec-workshop/blob/main/utils/evaluate.py). An example of how to run the evaluation script on your output file:

```bash
python ua-gec-workshop/utils/evaluate.py dev_corrected_sentences.txt --m2 ua-gec-workshop/data/dev/dev.m2
```

Under the hood, the script tokenizes your output with Stanza (unless
`--no-tokenize` provided) and calls [Errant](https://github.com/chrisjbryant/errant)
to do all the heavy lifting.

### Evaluation metrics

The script should give you an output like this:

```
=========== Span-Based Correction ============
TP      FP      FN      Prec    Rec     F0.5
107     18166   2044    0.0059  0.0497  0.0071
=========== Span-Based Detection =============
TP      FP      FN      Prec    Rec     F0.5
873     17393   1813    0.0478  0.325   0.0576
==============================================
```

Correction F0.5 is the primary metric used to compare results. In order to get a
true positive (TP), your rewrite must match both span and the suggested text of the annotator's rewrite.

To get a TP in span-based detection, it is enough to correctly identify
erroneous tokens. The actual correction doesn't matter here.

