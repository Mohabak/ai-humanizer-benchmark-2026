# AI Humanizer Benchmark 2026

An open, reproducible benchmark of popular AI humanizers. Each tool rewrote the same two AI-generated texts, and every output was scored by independent AI detectors. All inputs, outputs and raw scores are in this repo so anyone can check the numbers or rerun the test.

**Tested:** October 31, 2026
**Humanizers:** Walter Writes AI, Humanize AI (humanizeai.pro), Undetectable AI, QuillBot AI Humanizer, WriteHuman (partial)
**Detectors:** Proofademic, ZeroGPT, Sapling (all texts); Copyleaks and GPTZero (partial, usage limits)

## Results

![AI humanizer benchmark ranking](charts/ranking.png)

Ranked by how many detector checks each tool passed across the three core detectors (2 samples x 3 detectors = 6 checks). A check passes when the detector's AI score is below 50%.

| Rank | Humanizer | Checks passed | Avg AI score | Key points kept |
|---|---|---|---|---|
| 1 | Walter Writes AI | **6 / 6** | **14.2%** | 13 / 13 |
| 2 | Humanize AI (humanizeai.pro) | 4 / 6 | 41.9% | 11 / 13 |
| 3 | Undetectable AI | 1 / 6 | 78.2% | 13 / 13 |
| 4 | QuillBot AI Humanizer | 0 / 6 | 98.6% | 13 / 13 |
| n/a | WriteHuman (1 sample only) | 2 / 3 | 51.0% | 6 / 6 |
| baseline | Original AI text | 0 / 6 | 97.1% | n/a |

![Every detector score for every sample](charts/heatmap.png)

Average AI score per detector (lower = reads more human to that detector):

| Humanizer | Proofademic | ZeroGPT | Sapling | Copyleaks |
|---|---|---|---|---|
| Walter Writes AI | 19.5% | 18.1% | 4.8% | 0% (2 texts) |
| Humanize AI | 48.5% | 7.8% | 69.2% | n/a |
| Undetectable AI | 99.0% | 45.3% | 90.2% | n/a |
| QuillBot | 99.0% | 98.8% | 97.8% | 100% (1 text) |
| Original AI text | 98.5% | 100% | 93.0% | 100% |

### Per-text scores (AI probability)

| Text | Proofademic | ZeroGPT | Sapling | Copyleaks |
|---|---|---|---|---|
| `original-s1` | 99% | 100% | 96.2% | 100% |
| `original-s2` | 98% | 100% | 89.7% | 100% |
| `walter-s1` | 1% | 0% | 0.7% | 0% |
| `walter-s2` | 38% | 36.2% | 9% | 0% |
| `humanizeai-s1` | 2% | 0% | 39.3% | n/a |
| `humanizeai-s2` | 95% | 15.7% | 99.1% | n/a |
| `undetectable-s1` | 99% | 64.1% | 87.6% | n/a |
| `undetectable-s2` | 99% | 26.6% | 92.7% | n/a |
| `quillbot-s1` | 99% | 100% | 97.3% | 100% |
| `quillbot-s2` | 99% | 97.7% | 98.4% | n/a |
| `writehuman-s1` | 40% | 19.6% | 93.5% | n/a |

GPTZero scored `original-s1` as 100% AI before its scan limit was reached.

## What the numbers say

- **Walter Writes AI** was the only tool that got both samples past every detector. It passed all 6 core checks and both Copyleaks checks, and kept every key point. Outputs were 30% to 40% longer than the input.
- **Humanize AI** did very well on ZeroGPT and passed the academic sample everywhere, but Proofademic and Sapling flagged the blog sample. It also dropped the final sentence of both samples.
- **Undetectable AI** kept all the content but was flagged by Proofademic and Sapling on both samples. Its only pass was the blog sample on ZeroGPT.
- **QuillBot's humanizer** made light edits that kept the meaning but was flagged at 97% or higher on every check.
- **WriteHuman** asked for an account after one run, so it was only tested on one sample and isn't ranked.

## Method

1. **Samples.** Two AI-generated texts of 92 and 93 words, in different registers: academic (`s1`) and blog (`s2`). They were kept under 100 words because some humanizers cap input at 100 words, and every tool had to receive identical input. See [`samples/`](samples/).
2. **Baseline.** Every original sample was scored first. All detectors rated both as AI (89.7% to 100%).
3. **Humanizing.** Each sample was run once through each humanizer's web app with its default settings, and the first output was saved unedited in [`outputs/`](outputs/).
   - Walter Writes AI: Readability University, Purpose General, Bypass Level Enhanced (defaults), first draft.
   - Humanize AI (humanizeai.pro): Writing level Default, Tone Free, Rewrite level Balanced.
   - Undetectable AI: Readability University, Purpose General Writing, Human level Balanced.
   - QuillBot AI Humanizer: Standard mode.
   - WriteHuman: Standard model, sample 1 only.
4. **Detection.** Every output was pasted unedited into each detector's web app. Scores were recorded as the detector's AI probability (for Proofademic, 100 minus the stated human probability when the verdict was human). Raw results are in [`data/scores.csv`](data/scores.csv).
5. **Meaning check.** Each sample has 6 or 7 key points. A reviewer checked which points survived in each output and noted errors. See [`data/meaning.csv`](data/meaning.csv).
6. **Summary.** [`scripts/summarize.py`](scripts/summarize.py) recomputes [`data/summary.csv`](data/summary.csv) from the raw files.

```bash
python3 scripts/summarize.py
```

## Limitations

- **Small sample.** Two short texts per tool. Results show a direction, not a precise rate. Longer texts may score differently.
- **Single run.** Humanizers and detectors are not fully deterministic. Rerunning the same text can give different outputs and scores.
- **Detectors change.** Scores reflect each detector's model on the test date.
- **Detector usage limits.** Copyleaks and GPTZero stopped scoring after their usage limits, so they are reported but not used for ranking.
- **Meaning check is human judgment,** recorded with notes so it can be reviewed.

## Repository layout

```
samples/   original AI-generated texts (s1 academic, s2 blog)
outputs/   unedited humanizer outputs, named <tool>-<sample>.txt
data/      scores.csv (raw), meaning.csv, summary.csv
scripts/   summarize.py
charts/    ranking.png, heatmap.png
```

## License

Code is MIT licensed. Data and texts are released under CC BY 4.0. Tool names belong to their owners.
