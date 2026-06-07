# AI-Human Interaction Observatory

Field notes from a practitioner observing behavior in real AI-human interactions.

This is not a failure catalog. It is an ongoing record of patterns worth thinking about: how AI systems behave, and how humans respond to that behavior.

## The premise

The interesting questions about AI in production are not "does it work?" They are:

- How does the model behave when no one specified what it should do?
- What learned patterns emerge as defaults?
- How does the human notice, interpret, and react to those patterns?
- What does trust feel like when it is being built, or quietly eroded?

This observatory documents observations. Not bugs. Not failures. Behaviors that emerge in real interaction and deserve attention.

## What this produces

Observations alone are not the end product. Each observation is raw material for one of three outputs:

**1. A named pattern** — a behavior specific enough to describe, tag, and recognize in future interactions. This is the minimum output of every observation.

**2. A controlled experiment** — when a pattern is specific enough to test under reproducible conditions, it moves to [ai-eval-toolkit](https://github.com/cgarciamx80/ai-eval-toolkit). The experiment tests whether the observation holds outside the original context, and at what rate.

**3. An evaluation implication** — when a pattern has consequences for teams building AI products, it becomes input to evaluation design: a failure mode to cover, a rubric dimension to add, a test case category to include.

The pipeline:

```
Field observation
      |
Named behavioral pattern
      |
      +-- Controlled experiment (ai-eval-toolkit)
      |         |
      |     Reproducibility finding
      |
      +-- Evaluation implication
                |
            Rubric, test design, failure taxonomy
```

Not every observation reaches the experiment stage. Some patterns are real but not yet specific enough to test. Some require access or scale this project does not have. The observation record is the foundation; experiments and implications are built selectively on top of it.

## Observations

| # | Title | Experiment | Tags |
|---|-------|------------|------|
| [001](observations/001-prescribing-rest-without-evidence.md) | Prescribing rest without evidence | | prescription, closing-turn, calibration |
| [002](observations/002-template-voice-vs-translated-voice.md) | Template voice vs translated voice | | voice-mismatch, generation-defaults, collaboration |
| [003](observations/003-detecting-altered-states.md) | Detecting altered human states | | state-detection, signal-vs-noise, false-positive |
| [004](observations/004-confident-incomplete-delivery.md) | Confident incomplete delivery | | overconfidence, incomplete-output, trust-erosion |
| [005](observations/005-attributed-intelligence.md) | Attributed intelligence (mirror effect) | | attribution, mirror-effect, observer-cognition |
| [006](observations/006-asymmetric-theory-of-mind.md) | Asymmetric theory of mind | | theory-of-mind, asymmetry, reciprocity-illusion |
| [007](observations/007-silent-content-adaptation.md) | Silent content adaptation | | silent-adaptation, editorial-decisions, content-integrity |
| [008](observations/008-environment-dependent-skill-activation.md) | Environment-dependent skill activation | [Exp 001](https://github.com/cgarciamx80/ai-eval-toolkit/tree/main/experiments/001-skill-activation-reliability) | skill-activation, environment-dependence, qa-reliability |
| [009](observations/009-symmetric-expansion-behaviors.md) | Symmetric expansion behaviors | | expansion-behavior, behavioral-symmetry, conversational-dynamics |

## Who's observing

A single practitioner: **Carlos García**. 20 years in QA, currently working across multiple AI systems (Claude.ai, Claude Code, ChatGPT) in real working sessions. N=1, by design. Field notes, not academic study.

The value of N=1 is honesty: every observation is grounded in a specific moment, with a specific observer in a specific state. Aggregate studies miss the texture that makes these patterns visible in the first place.

## Methodology

Each observation follows a consistent structure:

- **Context:** when and where it happened
- **What was observed:** exact quotes when available
- **Observer's reaction:** what the human noticed and felt
- **Possible explanations:** hypotheses, not verdicts
- **Why this is interesting:** analytical relevance
- **How this might be studied further:** test designs for replication
- **Related observations:** links to other field notes

See [METHODOLOGY.md](METHODOLOGY.md) for the full approach.

## Why this exists

I have spent 20 years in software quality assurance. The frameworks I was trained in assume deterministic systems: there is a specification, the system either meets it or does not, and quality is measured against that gap.

LLMs and AI agents break that frame entirely. There is often no specification. The system behaves probabilistically. The most interesting failures are not violations of a spec; they are emergent patterns that nobody specified, that affect how humans trust and use the system.

This observatory is my attempt to develop frameworks for thinking about that newer kind of quality. It is incomplete, ongoing, and openly biased by my own observer state.

## Contact

Carlos García
- Email: carlos@holteck.com
- GitHub: [@cgarciamx80](https://github.com/cgarciamx80)

## License

CC BY 4.0. Attribution required. Feel free to reference, cite, and build on these observations. See [LICENSE](LICENSE) for details.
