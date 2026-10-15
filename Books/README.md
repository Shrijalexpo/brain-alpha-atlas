# Books and External Research References

Centralized library of third-party academic papers, quantitative finance books, formulaic Alpha collections, and official WorldQuant BRAIN reference captures.

> **Copyright and Licensing Notice:** Files stored in `Books/` are external third-party works and official platform captures retained for local research reference. They are excluded from public redistribution via `.gitignore` and are not covered by the repository's MIT or CC BY 4.0 licenses (see [`../NOTICE`](../NOTICE)). Original files are preserved unmodified with full attribution and SHA-256 provenance checksums.

## Directory Structure

```text
Books/
├── README.md                                  This catalog and metadata overview
├── books/                                     Textbooks and monographs on quantitative equity research
│   └── README.md                              Reading list and acquisition metadata
├── research-papers/                           Peer-reviewed and working papers on formulaic alphas
│   ├── README.md                              Paper abstracts, citations, and alpha translation notes
│   └── 1601.00991v3_101_formulaic_alphas.pdf  Kakushadze (2016), "101 Formulaic Alphas"
├── technical-guides/                          Executable/code-level factor and formula collections
│   ├── README.md                              Translation guide for Alpha101 and Alpha158
│   ├── alpha_101.txt                          101 Formulaic Alphas implementation reference
│   └── alpha_158.txt                          Qlib Alpha158 price-volume factor library
├── official-documentation/                    Official WorldQuant BRAIN platform and program references
│   ├── README.md                              Guide to captured official documentation
│   ├── india_wqbrain_formulaic_webpage_final_2022.pdf
│   ├── all_region_competition_2026_rules.txt
│   ├── worldquant_brain_operators_raw_capture.txt
│   └── brain-platform-docs/                   78 official BRAIN Learn articles + 142 figures
└── bibliographies/                            Master citation index, SHA-256 checksums, and literature map
    ├── reference_index.md                     File provenance, checksums, and storage locations
    └── quant_alpha_references.md              Annotated bibliography by research topic
```

## Complete Bibliographic Catalog

| Title | Author / Organization | Year | Venue / Source | Classification | Topic & Relevance to Alpha Research | Local Path |
|---|---|---:|---|---|---|---|
| *101 Formulaic Alphas* | Zura Kakushadze | 2016 | *Wilmott*, 2016(84), 72–81 ([arXiv:1601.00991v3](https://arxiv.org/abs/1601.00991)) | Academic | Canonical collection of 101 cross-sectional and time-series price-volume formulaic alphas; foundational operator patterns (`rank`, `ts_rank`, `correlation`, `decay_linear`) | [`research-papers/1601.00991v3_101_formulaic_alphas.pdf`](research-papers/1601.00991v3_101_formulaic_alphas.pdf) |
| *Alpha 101 Factor Implementation (`Alpha101`)* | WorldQuant / Open-Source Polars Port | 2016 | Community code port of Kakushadze (2016) | Community-produced | Expression-level reference for translating delay, correlation, and price-volume interaction terms into Fast Expression | [`technical-guides/alpha_101.txt`](technical-guides/alpha_101.txt) |
| *Alpha 158 Factor Library (`Alpha158`)* | Microsoft Research (Qlib) | 2020 | [Qlib Quantitative Platform](https://github.com/microsoft/qlib) (arXiv:2009.11189) | Academic / Community | 158 standardized candlestick (`KMID`, `KLEN`, `KUP`, `KLOW`), rolling price, rolling volume, and momentum/reversion features | [`technical-guides/alpha_158.txt`](technical-guides/alpha_158.txt) |
| *WorldQuant BRAIN India Base Fee & Formulaic Alpha Guide* | WorldQuant BRAIN | 2022 | Official WorldQuant BRAIN India Consultant Resource | Official | Base fee calculation methodology (Quantity Factor, Quality Factor, region/universe/correlation multipliers) and introductory formulaic alpha examples | [`official-documentation/india_wqbrain_formulaic_webpage_final_2022.pdf`](official-documentation/india_wqbrain_formulaic_webpage_final_2022.pdf) |
| *All Region Competition 2026 Official Guidelines* | WorldQuant, LLC | 2026 | WorldQuant BRAIN Platform Competition Terms (captured 2026-09-23) | Official | Eligibility rules, `RA Parent` + `Delay 1` scoring requirements, equal-weighted portfolio evaluation, and compliance/anti-noise rules | [`official-documentation/all_region_competition_2026_rules.txt`](official-documentation/all_region_competition_2026_rules.txt) |
| *WorldQuant BRAIN Learn Documentation Archive (78 Articles)* | WorldQuant BRAIN | 2026 | `https://platform.worldquantbrain.com/learn/documentation` (captured 2026-06-28 / 2026-10-09) | Official | Complete offline reference of 78 platform tutorials across 11 topics (Discover BRAIN, Create Alphas, Examples, Interpret Results, Data, Advanced Topics, Regions, Consultant Info, BRAIN API, SuperAlpha, Themes) + 142 figures | [`official-documentation/brain-platform-docs/index.md`](official-documentation/brain-platform-docs/index.md) |
| *WorldQuant BRAIN Operator Reference Capture* | WorldQuant BRAIN | 2026 | `https://platform.worldquantbrain.com/learn/data-and-operators/operators` (captured 2026-07-24) | Official | Raw offline capture of platform operator signatures, descriptions, and parameters (curated in [`../Docs/05-fast-expression-language/operator-reference.md`](../Docs/05-fast-expression-language/operator-reference.md)) | [`official-documentation/worldquant_brain_operators_raw_capture.txt`](official-documentation/worldquant_brain_operators_raw_capture.txt) |

## Cross-Links

- **Curated Consultant Curriculum:** [`../Docs/index.md`](../Docs/index.md)
- **Simulation & Experiment Evidence:** [`../Analysis and Simulation Reports/index.md`](../Analysis%20and%20Simulation%20Reports/)
- **Research Utilities & Parsers:** [`../Tools/README.md`](../Tools/README.md)
