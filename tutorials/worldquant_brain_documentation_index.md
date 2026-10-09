# WorldQuant BRAIN Documentation Index

Source: captured from the logged-in BRAIN Learn section using Computer Use on 2026-07-26, plus a clean text capture of the consultant and competition pages on 2026-10-06.

Raw captures are stored in:

```text
tutorials/worldquant_brain_documentation_raw/
Operators/worldquant_brain_operators_raw_capture.txt
```

The raw captures are browser accessibility text. They are useful as source material, but curated notes should be preferred for daily alpha work.

## Documentation Sections Captured

### Discover BRAIN

- `*Read this First* - Starter Pack`
- `Introduction to Alphas`
- `Introduction to BRAIN Expression Language`
- `Intermediate Pack - Understand Results [1/2]`
- `Intermediate Pack - Improve your Alpha [2/2]`
- `10 Steps to Start on BRAIN`
- `WorldQuant Challenge`

### Create Alphas

- `Simulate your first Alpha`
- `Test Period`
- `How to choose the Simulation Settings`
- `How BRAIN works`

### Examples

- `Alpha Examples for Beginners`
- `Alpha Examples for Bronze Users`
- `Alpha Examples for Silver Users`

### Interpret Results

- `Clear these tests before submitting an Alpha`
- `Parameters in the Simulation results`

### Understanding Data

- `Understanding Data in BRAIN: Key Concepts and Tips`
- `How to use the Data Explorer`
- `Vector Data Fields`
- `Group Data Fields`
- `Getting Started with Option6 Implied volatility (IV)`

### Advanced Topics

- `Must-read posts: How to improve your Alphas`
- `Neutralization`
- `D0`

### Consultant Information

- `Osmosis Allocation Guide for Consultants`
- `Research Advisory Program`
- `Consultant Simulation Features` (Multi-Simulation, Test Period)
- `Visualization Tool`
- `Consultant Dos and Don'ts`
- `Build Alphas using research papers`
- Navigation lists `Research Advisory Program` and `Your Advisor - Sarthak Shrivastava`

### Competitions

- `SPC 2026 - Systematic Prediction Challenge` (Help Center > SPC 2026 > Structure)

### Consultant Resources (Help Center)

- `Alpha Creation Engine - API library [Gold]`
- `FAQs on ILLIQUID_MINVOL1M Universes`
- `Getting Starting Guide for WorldQuant Brain Research Consultants`
- `A list of must-read posts on how to improve your Alphas that are submitted`
- `What happens if a dataset gets removed from Brain?`
- `What is BRAIN Labs and how is it useful to me?` / `How can I access BRAIN Labs?`

### Regions And Universes

- `Global Alphas [Gold]`
- `USA TOPSP500 universe [Gold]`
- `GLB TOPDIV3000 Universe`
- `USA TOP2000, ASI MINVOL10M, ASI TOP500, GLB MINVOL10M Universe`
- `HKG/KOR/TWN [Grand Master]`
- `EUR TOP2500 Universe`
- `EUR TOPCS1600 Universe`
- `AMR Alphas [Master]`
- `JPN Alphas [Master]`
- `China Alphas: Understand the market`
- `GBR/DEU`
- `India Alphas`

### Consultant Tutorial Task Pages

- `Regular Alpha` (IS Ladder test, Prod-Correlation test)
- `ATOM` (Single Dataset Alphas)
- GLB TOPDIV3000 thematic competition notice (GLB/D1 Liquid Power Pool Aug'26)

Note: the entries above were captured on 2026-10-06 as clean pasted text rather than browser accessibility dumps, so they have curated notes but no files under `worldquant_brain_documentation_raw/`. All consultant-only material is curated in `tutorials/consultant_information/`.

## Course Index Captured

Courses visible in the Learn section:

- `Quantcepts` - 19 lessons. Concepts such as alphas, factor risks, market neutrality, options data, sentiment, fundamentals, and broader investment research.
- `Introduction to Quantitative Finance` - 3 lessons. Quant research ecosystem and alpha process.
- `Alpha Examples by Data Category` - 2 lessons. Examples across data categories.
- `Alpha Examples by Idea type and Delay` - 2 lessons.
- `Combining Alphas and Risk Management` - 2 lessons. Diversity across models, data categories, time horizons, techniques, and risk management.
- `Implementing Advanced Ideas on BRAIN` - 2 lessons. Advanced data and deep learning ideas.
- `Introduction to WorldQuant BRAIN` - 3 lessons.
- `International Quant Championship 2026` - 3 lessons.
- `Introduction to Alphas` - 6 lessons.
- `Basic Operators` - 4 lessons.

## Most Important Curated Notes

Use these curated files first:

```text
Operators/worldquant_brain_operator_reference.md
tutorials/worldquant_brain_platform_docs_summary.md
Data/data_explorer_and_field_research.md
Research/neutralization_guidelines.md
Research/alpha_improvement_from_docs.md
tutorials/consultant_program_osmosis_allocation_guide.md      (local only, not published)
tutorials/spc_2026_prompt_competition.md                      (local only, not published)
tutorials/consultant_information/README.md                    (local only, not published)
tutorials/consultant_information/submission_tests_and_alpha_types.md   (local only, not published)
tutorials/consultant_information/regions_and_universes.md     (local only, not published)
tutorials/consultant_information/alpha_research_practices.md  (local only, not published)
tutorials/consultant_information/platform_features.md         (local only, not published)
```

`(local only, not published)` marks material governed by the platform's own program terms. It is
kept on the authoring machine and excluded from this public repository by `.gitignore`; the wiki
records the general lessons from it in [`docs/`](../docs/index.md).

## Consultant-Only Knowledge Base

The consultant material is large enough to warrant its own folder. Start here:

```text
tutorials/consultant_information/README.md
```

It indexes the consultant-level submission tests (IS Ladder, prod-correlation), the alpha types (Regular, ATOM, Power Pool, SuperAlpha), all region and universe guidance with per-region thresholds, the operating and research guidelines, and the platform features (Multi-Simulation, Test Period, Visualization Tool, ACE API).

## Consultant And Competition Notes

Beyond Alpha research, the workspace now tracks the consultant-side mechanics:

```text
tutorials/consultant_program_osmosis_allocation_guide.md   (local only, not published)
tutorials/spc_2026_prompt_competition.md                    (local only, not published)
competition_contract.txt                                    (local only, not published)
Books/References/worldquant_official/india_wqbrain_formulaic_webpage_final_2022.pdf   (local only, not published)
```

The items above are program terms, program mechanics and reference documents that this repository
does not redistribute. They are retained locally for the author's own research; see
[the evidence policy](../docs/15-sources-and-policy.md) for why.

Supporting tool:

```text
Tools/validate_spc_isin.py         Dependency-free ISIN/MIC and JSON sample-output validator (has --selftest)
Tools/spc_sample_output_example.json  Official SPC sample output used as the validation fixture
```

