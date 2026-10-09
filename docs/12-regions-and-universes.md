# Regions and Universes

Region and universe are research scope, not settings you optimise later. A result belongs to the
combination of region, universe, delay, decay and neutralisation it was measured under — change
any of them and you have a new question.

## Region

The region is the market you trade. Regions visible in the platform documentation captured for
this repository include USA, EUR, ASI, CHN, GLB/ALL, AMR, JPN, HKG/KOR/TWN, GBR/DEU and India,
along with region-agnostic ("RA"/global) alpha types. `[Platform]`

| Region | What the recorded evidence shows |
|---|---|
| **USA** | The most explored scope here and the most crowded. The submitted family is USA. Recent sweeps show the surface has moved: failures are now book geometry and robustness, not signal strength |
| **EUR** | 4,223 blocks across three sweeps, 0 passes. `LOW_2Y_SHARPE` and `LOW_SUB_UNIVERSE_SHARPE` dominate; the best risk-adjusted pocket is slow analyst level fields with time-series scaling |
| **AMR** | 3,250 blocks, 0 passes, 25 `PENDING`. Model value-momentum ranks looked promising (~1.6 Sharpe / ~1.4 Fitness at ~7% turnover) but the leaders were unevaluated |
| **KOR** | 789 blocks, 0 passes. The strongest single block in this repository's recent record (Sharpe 2.36 / Fitness 1.67) failed only the 2-year check. `LOW_2Y_SHARPE` fails 96.5% of KOR blocks |
| **ALL / GLB (LARGE)** | 192 blocks, 0 passes, best Fitness 0.57. Introduces sub-region checks (Asia/Japan, Americas, EMEA) that a global alpha must satisfy |
| **CHN, JPN, ASI, IND** | Present in the platform documentation; no meaningful recorded experiments in this repository. Treat as untested here |

An important pattern: **the same field list behaved completely differently by region.** Analyst
prefixes that formed the best EUR pocket were weak in USA, and universes below TOP2500 collapsed
in EUR while TOP3000 carried the USA results. `[Observed]`

## Universe

The universe is the instrument set inside the region. Larger universes are generally easier for
cross-sectional signals — more names means a thicker cross-section, more balanced groups, and
better sub-universe robustness — but they also include instruments that are harder to trade at
size. `[Platform]`

Recorded evidence: `[Observed]`

| Observation | Detail |
|---|---|
| Bigger is easier | In the USA page, all 12 blocks above Sharpe 1.25 came from TOP3000; TOP200/500/1000/2000/TOPSP500 produced none on the same field list |
| Smaller universes collapse in EUR | In the EUR sweeps, universes below TOP2500 performed materially worse than TOP2500 |
| Small universes are their own surface | EUR TOPCS1600 produced a best decay-5 result of 0.82 Sharpe while the decay-0 work on it reached 1.82 / 1.41 |
| Region-universe pairs are specific | KOR TOP600, AMR TOP600 and USA TOP3000 each behaved according to their own name counts — a 600-name universe concentrates weight far more easily than a 3,000-name one |

## What this means in practice

- **Test the universe you intend to submit in.** A result on TOP3000 is not evidence for TOP600.
- **Expect concentration problems in small universes.** With 600 names, a few extreme scores move
  a large share of the book; rank, winsorise and truncate aggressively. `[Notes]`
- **Expect sub-universe failures to be about tails.** If the alpha earns its edge in names that
  exist in TOP3000 but not in the sub-universe, the check is telling you something real. `[Notes]`
- **Re-verify a ported idea from scratch.** Same prefix, different region does not mean same
  economic field. `[Observed]`

## Region-agnostic and ALL-scope alphas

The ALL/global scope is not simply "the union of regions". The recorded GLB pages show the
platform evaluating the alpha per sub-region as well as in aggregate, with checks such as
`LOW_GLB_APAC_SHARPE`, `LOW_ASI_JPN_SHARPE`, `LOW_GLB_AMER_SHARPE`, `LOW_GLB_EMEA_SHARPE`,
`LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` and `LOW_ROBUST_UNIVERSE_RETURNS`. `[Observed]`

The practical implication: an alpha that is excellent in one region can be mediocre globally, and
the global checks will find out. The recorded GLB blocks were the weakest in the bundle — best
Sharpe 1.42 with Fitness 0.57 across 192 blocks. `[Observed]`

The platform documentation describes region-agnostic ("RA"/global) alpha types and parent-child
relationships between global and regional alphas. That material is captured in the repository's
consultant notes; the mechanism is described at a conceptual level in
[Advanced topics](14-advanced.md), without reproducing program-specific requirements that change
over time. `[Platform]`

## Region-specific submission criteria

Submission criteria are **not** uniform across regions, and this is true at both the user level
and the consultant level. The recorded evidence shows the practical effect directly: AMR/TOP600
blocks at Sharpe 1.4–1.6 failed `LOW_SHARPE`, while USA blocks at comparable Sharpe cleared it.
`[Observed]`

The platform's authoritative statement of the criteria for your region is the check list shown
with your own simulation. Consultant-program material adds further gates (a window-by-window
consistency ladder and a production-correlation requirement); that material is consultant-scoped
and is **not reproduced in this wiki** — see the explanation in
[Sources and evidence policy](15-sources-and-policy.md).

## A note on competition- and program-specific rules

Competitions and consultant programs have their own eligibility, scoring and timing rules that
change between seasons. Nothing in this wiki should be read as a statement of current competition
terms. Where such material exists in this repository, it is kept with its original date and
treated as historical. `[Notes]`

Next: [Tools and API](13-tools-and-api.md) · [Advanced topics](14-advanced.md).
