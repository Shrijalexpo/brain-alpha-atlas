# Raw Simulation Export Source Data

Archived raw text exports from WorldQuant BRAIN multi-simulation pages. Kept separate from parsed CSV/JSON/Markdown outputs to guarantee full reproducibility.

## Stored Raw Exports

| File | Experiment ID | Pages | Blocks | Size (Bytes) | MD5 Checksum | Original Source |
|---|---:|---:|---:|---:|---|---|
| [`20261008_071542.txt`](20261008_071542.txt) | `070` | 2 | 3,550 (`2,500 + 1,050`) | 1,016,886 | `3a92f8e8980c9b789778aaad65528b9f` | `~/Downloads/Simulation Results.rtf` (MD5 `1b461cf245bd7fadbd3f42d812389e3f`) |
| [`20261009_115500.txt`](20261009_115500.txt) | `071` | 6 | 5,546 (`789 + 3,250 + 1,141 + 113 + 174 + 79`) | 1,601,293 | `485d8962d27370eda1bbbdde118bd322` | `~/Downloads/Simulation .rtf` (MD5 `862d3bacb18569ae2aea90cc6717c493`) |

## Reproducing Parsed Sweep Artifacts

Run [`../../Tools/simulation-processing/brain_sweep_parser.py`](../../Tools/simulation-processing/brain_sweep_parser.py) from the repository root:

```bash
python3 Tools/simulation-processing/brain_sweep_parser.py \
  "Analysis and Simulation Reports/source-data/20261008_071542.txt" \
  --outdir "Analysis and Simulation Reports/sweeps-and-experiments" \
  --prefix 20261008_071542_

python3 Tools/simulation-processing/brain_sweep_parser.py \
  "Analysis and Simulation Reports/source-data/20261009_115500.txt" \
  --outdir "Analysis and Simulation Reports/sweeps-and-experiments" \
  --prefix 20261009_115500_
```
