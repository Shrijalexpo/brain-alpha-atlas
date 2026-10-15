# Research Papers

Peer-reviewed and working papers stored for WorldQuant BRAIN Alpha hypothesis generation.

## Stored Papers

### 1. *101 Formulaic Alphas* (Kakushadze, 2016)

- **File:** [`1601.00991v3_101_formulaic_alphas.pdf`](1601.00991v3_101_formulaic_alphas.pdf)
- **Author:** Zura Kakushadze
- **Publication Year:** 2016
- **Venue:** *Wilmott*, 2016(84), 72–81
- **Source URL:** https://arxiv.org/abs/1601.00991
- **Classification:** Academic
- **SHA-256 Prefix:** `1f9c21afe32dcb3e...`
- **Relevance to Alpha Research:**
  - Provides 101 explicit real-world price-volume formulaic alphas with average holding periods of 0.6–6.4 days.
  - Demonstrates cross-sectional vs time-series operator nesting (`rank`, `ts_rank`, `correlation`, `covariance`, `decay_linear`, `IndNeutralize`).
  - **Caution:** Do not submit verbatim Alpha#1–Alpha#101 expressions on BRAIN; they are heavily crowded and fail production-correlation checks. Use them as structural templates to adapt onto less crowded datasets (`anl69`, `option6`, `model77`) or regions (`EUR`, `GLB`, `KOR`, `AMR`).
