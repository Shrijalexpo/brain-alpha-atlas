# Research Workflow

A repeatable loop for turning an idea into a credible alpha candidate. This is the process the
recorded experiments followed, written as instructions rather than principles.

## The loop

```text
1. Hypothesis   one sentence, written before the simulator is opened
2. Field        a field that can actually express the hypothesis; check coverage and type
3. Baseline     the simplest expression that tests it; simulate
4. Diagnose     read the metrics AND the failed checks; name the ONE binding constraint
5. One change   change a single mechanism, not several
6. Record       write the result, settings and lesson into the ledger
7. Compare      judge against the baseline under identical settings
8. Decide       improve, abandon, or move to robustness and correlation work
```

The loop is only useful if steps 4 to 7 are done honestly. Skipping step 6 is what turns a
research programme into a random walk.

## Step 1 — Write the hypothesis first

One sentence, in economic language, with a direction:

```text
Good:  Companies whose estimated earnings are being revised upward should outperform peers
       over the following month, because revisions diffuse slowly into prices.

Bad:   Try anl10 fields with ts_rank.
```

The bad version cannot be evaluated — when it fails, you learn nothing except "that didn't
work". The good version tells you what to change if it fails (a different diffusion window, a
different revision measure) and what would falsify it.

## Step 3 — Keep the baseline small

A baseline with one or two terms tells you which part carries signal. A baseline with five
terms cannot fail informatively.

| Baseline size | What a failure tells you |
|---|---|
| One term | That field/transform has no edge in this region |
| Two terms | Which of the two is dragging, by dropping one |
| Five terms | Almost nothing — you cannot attribute the weakness |

The recorded record is full of cautionary examples of the failure mode: a large linear
quality/value composite returned negative Sharpe, a multiplicative profitability/cashflow
interaction returned −1.01, and repeated attempts to rescue a weak branch by stacking more
similar factors produced progressively worse results. `[Observed]`

## Step 4 — Name the single binding constraint

Read the metrics **and** the check list, and write down one sentence: what is actually stopping
this?

| Reading | Binding constraint | Next move |
|---|---|---|
| Sharpe below bar, turnover fine | Signal is weak | Change the idea, field or transform |
| Sharpe good, Fitness low, turnover high | Cost of trading | Smooth the fastest component or raise Decay |
| Sharpe good, Fitness low, turnover low | Returns too small for the risk taken | Increase signal strength selectively |
| Sharpe good, `CONCENTRATED_WEIGHT` fails | Book geometry | Rework grouping, truncation, or the number of buckets |
| Sharpe good, robustness checks fail | Regime or universe dependence | Test before submitting; may be unsalvageable |
| Negative Sharpe | Direction or construction | Question the construction before inverting it |

A worked example of why "name one" matters: in the USA implied-volatility family, decay 4, 6 and
8 all failed the same two checks. `[Observed]` The binding constraint was weight concentration,
not smoothing — so every decay sweep was wasted effort. Naming the constraint would have
redirected the work to the book construction immediately.

## Step 5 — Change one thing, and say why

Before running the variant, state the mechanism you are changing and the result you expect:

```text
Change: add group_rank(..., subindustry) instead of plain rank
Expect: lower weight concentration, small Sharpe cost
```

This is what makes an experiment an experiment. Two changes at once, and a good result leaves
you unable to say which change caused it.

## Step 6 — Record before you iterate

Every experiment gets a record and a ledger row. The minimum useful record is: ID, date,
expression, settings, metrics, failed checks, conclusion, lesson, next action — the template in
[`simulations/simulation_template.md`](../simulations/simulation_template.md). `[Notes]`

Two rules that have earned their place in this repository: `[Observed]`

- **Record the settings.** A Sharpe without region, universe, delay, decay, truncation and
  neutralisation is not a result.
- **Quote the out-of-sample numbers.** The recorded USA sweep had `Train Sharpe` and `Sharpe`
  disagreeing in 2,448 of 2,500 blocks, with the training column systematically higher. Mixing
  the two inflated a headline number by 0.29 and nearly changed a conclusion.

## Step 7 — Compare fairly

Only compare variants run under identical settings. A variant at decay 8 is not comparable with
a baseline at decay 4 unless you also ran the baseline at decay 8 — and the recorded evidence
shows decay moves turnover far more than it moves Sharpe, so a turnover difference is usually
a settings artifact, not a signal finding. `[Observed]`

## Step 8 — Decide

Three outcomes, and you should be able to defend which one applies: `[Notes]`

```text
IMPROVE     the constraint is addressable and the idea is still supported
ABANDON     the idea survived several controlled changes without improving, or the economics
            no longer hold; record why so the family is not re-tried blindly
ESCALATE    metrics clear the thresholds; move to robustness, test period, and correlation work
```

Abandoning is a result. A recorded, reasoned abandonment saves the next researcher a day.

## What makes research inefficient

Worth stating explicitly, because these are the common ways simulation budget disappears:
`[Notes]`

| Anti-pattern | Why it fails |
|---|---|
| Random operator combinations | No hypothesis, so no way to learn from failure |
| Repeatedly tweaking one weak signal | If the base signal is weak, variants of it are weak |
| Tuning settings to fix a weak idea | Settings express an idea; they rarely create signal |
| Stacking many correlated factors | Dilutes the strongest component and obscures attribution |
| Reversing a signal to improve a number | Contradicts the economic reasoning behind the construction |
| Judging on train-period numbers | Overstates performance; use the test period |

## A worked mini-example

```text
1. Hypothesis   Earnings revisions diffuse slowly, so upward revisions predict outperformance
                over the following weeks.
2. Field        An analyst revision score with broad coverage.
3. Baseline     zscore(ts_backfill(revision_score, 21))
4. Read         Sharpe near 1.26, Fitness 1.03, turnover 5.38% - clears Fitness but fails
                LOW_SHARPE and CONCENTRATED_WEIGHT.
5. One change   Address the concentration: rank instead of zscore, or neutralise within a
                size bucket. Not: raise decay, which will not touch concentration.
6. Record       Save both the baseline and the variant, with settings and the failed checks.
```

That example is drawn from a recorded KOR-scope block. `[Observed]` Note how step 4 already
identifies the next move: the constraint is book geometry, so smoothing would be wasted work.

## Where to go next

- [Evaluating results](07-evaluating-results.md) — reading the numbers correctly
- [Failed checks](08-failed-checks.md) — what each failure means
- [Improving alphas](09-improving-alphas.md) — the repair catalogue
- [Experiment index](10-experiment-index.md) — check whether the idea is already recorded
