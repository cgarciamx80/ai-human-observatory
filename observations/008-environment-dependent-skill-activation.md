---
observation_id: 008
type: observation
status: preliminary — pending work-machine evidence
date: 2026-05-23
observer: Carlos García
source: Cross-environment comparison (personal machine + work machine, Claude Code)
domain: ai-human-interaction, ai-collaboration, qa-ai-assisted
tags: [skill-activation, environment-dependence, partial-compliance, qa-reliability, reproducibility]
---

# Observation 008: Environment-Dependent Skill Activation

## Context

Claude Code supports registered custom Skills: Markdown-defined instructions
that the model is expected to invoke automatically when a relevant prompt
arrives. The observer has been using Skills in two distinct environments:

- **Personal machine:** Controlled sessions. Working directory set explicitly
  to the experiment folder. Clean sessions per run.
- **Work machine (Instructure):** Real working sessions. Accumulated context.
  Multiple concurrent tasks. No explicit session management between uses.

Controlled experiment data exists for the personal machine environment:
Experiment 001 (Skill Activation Reliability, 10 runs, May 2026) showed
100% marker presence across both clean and noisy session conditions.

The work machine tells a different story.

## What Was Observed

On the work machine, the observer has repeatedly seen Skills fail to
activate when expected. The behavior appears in two forms:

- **Full skip:** The model completes the task with no evidence of skill
  invocation. No marker, no skill-defined formatting, no acknowledgment.
- **Partial compliance:** The model produces output that follows some skill
  formatting rules but not others — identical to the has_total_time failure
  pattern documented in Experiment 001, but appearing more broadly across
  different skills and task types.

The same skill definition, the same trigger prompt, different environment,
different result.

Critically: the observer has not been able to reproduce the work-machine
skips in the controlled personal-machine environment. The controlled
environment shows near-perfect activation. The uncontrolled real environment
shows intermittent failure.

**Status:** Full skip and partial compliance instances have been observed
repeatedly but not yet formally documented with timestamps and diagnostic
data. This observation is preliminary pending structured evidence collection
on the work machine.

## Why This Has Two Implications

### 1. LLM behavioral research angle

Skill activation is not a deterministic function of the prompt alone.
The environment — session state, working directory, accumulated context,
possibly model version — appears to influence whether a registered skill
fires. This means:

- Controlled experiments on skill behavior may not generalize to
  production conditions.
- Experiment 001's 100% activation rate may reflect controlled-environment
  artifact more than true model reliability.
- The interesting variable is not "does the skill activate given prompt X"
  but "under what environmental conditions does skill activation become
  unreliable?"

### 2. AI-assisted QA angle

If a QA practitioner builds a workflow around Skills (structured test plan
format, required output markers, consistent field completion), intermittent
activation makes that workflow unreliable. The practitioner cannot trust
that a skill-dependent output will consistently meet the structural
requirements they depend on for downstream use.

This is a QA reliability problem embedded in the AI layer: the tool
behaves differently in production than in testing. A pattern familiar
to any QA engineer, now appearing in the AI assistant itself.

## Possible Explanations

1. **Working directory mismatch:** Skills load relative to the working
   directory. If the work machine session is not anchored to the folder
   containing the `.claude/skills/` directory, the skill is invisible
   to the model regardless of prompt.

2. **Context interference at scale:** The work machine has longer,
   denser sessions with more accumulated context. The noise-condition
   results from Experiment 001 (5 prior prompts) may underestimate the
   interference effect at real-world session scale (20-50+ prior exchanges).

3. **Model version drift:** Claude Code may serve different model versions
   across machines or across time. If the work machine is running a
   different version, activation behavior may differ independently of
   session conditions.

4. **Skill definition visibility:** If the skill file is not in the
   expected path relative to the active working directory, the model
   never sees the definition and cannot invoke what it does not know exists.

## How This Might Be Studied Further

**Immediate diagnostic (work machine):** After observing a skip, run
the diagnostic prompt below to capture what the model sees about its
own skill environment without exposing project content.

**Structured replication:** Run Experiment 001 conditions on the work
machine. Compare activation rates across identical conditions in both
environments. If personal machine = ~100% and work machine = lower,
the gap is the finding.

**Variable isolation:** Test each candidate explanation independently:
- Verify working directory before each run
- Control for session length
- Log model version across runs

## Related Observations

- [Observation 007](007-silent-content-adaptation.md): Both involve the model
  doing something other than what was expected without disclosure. 007 is about
  content modification; 008 is about tool invocation failure.
- [Experiment 001](https://github.com/cgarciamx80/ai-eval-toolkit) (private):
  The controlled dataset that makes the work-machine divergence visible.
  Without Experiment 001 as a baseline, the work-machine behavior would
  have no comparison point.

## Notes

This observation sits at the intersection of two disciplines:
LLM behavioral research and QA engineering. The environment-dependence
pattern is immediately legible to any QA professional who has seen a
test pass in staging and fail in production. The framing transfers.

Evidence collection on the work machine is the next required step before
this observation can be marked as fully documented.
