"""Summarize the benchmark: average AI score and pass rate per humanizer and detector.

A humanized text "passes" a detector when the detector's AI score is below 50%.
Core detectors are the three that scored every text: Proofademic, ZeroGPT and Sapling.
"""
import csv
import collections
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORE = ("proofademic", "zerogpt", "sapling")
PARTIAL = {"writehuman"}  # free tier stopped after one sample; reported, not ranked
PASS_BELOW = 50.0


def main() -> None:
    scores = collections.defaultdict(lambda: collections.defaultdict(list))
    with open(ROOT / "data" / "scores.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tool = row["text"].rsplit("-", 1)[0]
            scores[tool][row["detector"]].append(float(row["ai"]))

    meaning = collections.defaultdict(lambda: [0, 0])
    with open(ROOT / "data" / "meaning.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tool = row["text"].rsplit("-", 1)[0]
            meaning[tool][0] += int(row["key_points_kept"])
            meaning[tool][1] += int(row["key_points_total"])

    rows = []
    for tool, by_det in scores.items():
        core = [x for d in CORE for x in by_det.get(d, [])]
        if not core:
            continue
        avg = sum(core) / len(core)
        passed = sum(x < PASS_BELOW for x in core)
        kept, total = meaning.get(tool, (0, 0))
        per_det = {d: round(sum(v) / len(v), 1) for d, v in by_det.items()}
        rows.append((tool, round(avg, 1), passed, len(core), kept, total, per_det))

    rows.sort(key=lambda r: (r[0] == "original", r[0] in PARTIAL, -r[2] / r[3], r[1]))
    out = ROOT / "data" / "summary.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tool", "ranked", "core_avg_ai_score", "core_passes", "core_checks",
                    "key_points_kept", "key_points_total", "per_detector_avg"])
        for r in rows:
            w.writerow([r[0], "no" if r[0] in PARTIAL or r[0] == "original" else "yes", r[1], r[2], r[3], r[4] or "", r[5] or "",
                        "; ".join(f"{k}={v}" for k, v in r[6].items())])
    for r in rows:
        print(f"{r[0]:<13} avg AI {r[1]:>5}%  passes {r[2]}/{r[3]}  meaning {r[4]}/{r[5]}  {r[6]}")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
