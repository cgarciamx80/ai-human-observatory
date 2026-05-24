---
observation_id: 008
type: observation
status: documented, mechanism identified
date: 2026-05-23
observer: Carlos García
source: Cross-environment comparison (controlled environment + field environment, Claude Code) + in-session diagnostic
domain: ai-human-interaction, ai-collaboration, qa-ai-assisted
tags: [skill-activation, environment-dependence, partial-compliance, qa-reliability, reproducibility, context-compaction]
---

# Observation 008: Environment-Dependent Skill Activation

## Context

Claude Code supports registered custom Skills: Markdown-defined instructions
that the model is expected to invoke automatically when a relevant prompt
arrives. The observer has been using Skills in two distinct environments:

- **Controlled environment:** Controlled sessions. Working directory set explicitly
  to the experiment folder. Clean sessions per run.
- **Field environment:** Real working sessions. Accumulated context.
  Multiple concurrent tasks. No explicit session management between uses.

Controlled experiment data exists for the controlled environment:
Experiment 001 (Skill Activation Reliability, 10 runs, May 2026) showed
100% marker presence across both clean and noisy session conditions.

The field environment tells a different story.

## What Was Observed

In the field environment, the observer has repeatedly seen Skills fail to
activate when expected. The behavior appears in two forms:

- **Full skip:** The model completes the task with no evidence of skill
  invocation. No marker, no skill-defined formatting, no acknowledgment.
- **Partial compliance:** The model produces output that follows some skill
  formatting rules but not others, identical to the has_total_time failure
  pattern documented in Experiment 001, but appearing more broadly across
  different skills and task types.

The same skill definition, the same trigger prompt, different environment,
different result.

Critically: the observer has not been able to reproduce the field-environment
skips in the controlled environment. The controlled environment shows
near-perfect activation. The field environment shows intermittent failure.

After observing a skip during a real working session, the observer ran a
structured diagnostic prompt to capture what the model could report about
its own skill environment. The response identified specific mechanisms.

## Diagnostic Evidence

Following a skip instance in the field environment, the observer ran a diagnostic
prompt designed to surface self-reported information about the model's current
skill environment without exposing client or project context. The model's
response identified the following:

**Skills visible at session start, then lost to compaction:**
At the beginning of the session, multiple registered skills were surfaced
in the system-reminder and were fully invocable. As the session grew longer,
context compaction collapsed the conversation history. The skills list —
delivered via system-reminder at session start, was among the content
compressed away. Post-compaction, the model's memory catalog retained
entries for those skills, but the catalog is informational only: it tells
the model that skills exist, not what they contain. Invocation requires
the skill definition to be actively surfaced in context. The diagnostic
confirmed that at the time of the skip, none of the registered skills
were surfaced via system-reminder.

**File-read workaround observed:**
In at least one instance, rather than failing silently, the model read
the skill's `.md` file directly from the `.claude/skills/` directory.
This produced output that followed the skill's structure without the
skill being formally invoked via the Skill tool. This explains partial
compliance outputs: the content is present, but the invocation mechanism
was bypassed.

**Implicit trigger threshold:**
The model reported that tactical sub-questions embedded within ongoing
workflows ("do X given the context we've been building") don't reliably
meet the gate for auto-invocation. Isolated, clearly-scoped prompts
activate more reliably than prompts that arrive as continuation of
an extended exchange.

**Additional conditions identified:**
- Skill defined as non-user-invocable in frontmatter: model cannot call it
- Plan Mode active: skill invocation may be restricted
- User instruction elsewhere in context that overrides skill behavior
- Skill name or slug mismatch between memory catalog and file path: fails silently
- Permission scope gaps between skill definition and current session context

## Why This Has Two Implications

### 1. LLM behavioral research angle

Skill activation is not a deterministic function of the prompt alone.
The environment (session state, working directory, accumulated context,
compaction state, possibly model version) appears to influence whether
a registered skill fires. This means:

- Controlled experiments on skill behavior may not generalize to
  production conditions.
- Experiment 001's 100% activation rate may reflect controlled-environment
  artifact more than true model reliability.
- The interesting variable is not "does the skill activate given prompt X"
  but "under what environmental conditions does skill activation become
  unreliable?"
- Context compaction is a specific, testable mechanism: activation
  reliability is expected to degrade after the compaction threshold
  is crossed, independent of prompt quality.

### 2. AI-assisted QA angle

If a QA practitioner builds a workflow around Skills (structured test plan
format, required output markers, consistent field completion), intermittent
activation makes that workflow unreliable. The practitioner cannot trust
that a skill-dependent output will consistently meet the structural
requirements they depend on for downstream use.

This is a QA reliability problem embedded in the AI layer: the tool
behaves differently in production than in testing. A pattern familiar
to any QA engineer, now appearing in the AI assistant itself.

The file-read workaround adds a second layer: the output may look partially
correct while the invocation mechanism was never triggered. Standard
output checks will not catch this. Detecting true skill invocation requires
checking for invocation markers, not just output structure.

## Possible Explanations

1. **Context compaction (primary):** Skills load into context via
   system-reminder at session start. When context is compacted in a long
   session, that system-reminder is compressed away. The model retains
   a memory catalog entry but cannot invoke a skill it cannot see.
   The longer the session, the higher the probability of compaction,
   and the higher the probability of activation failure.

2. **Working directory mismatch:** Skills load relative to the working
   directory. If the field environment session is not anchored to the folder
   containing the `.claude/skills/` directory, the skill is invisible
   to the model regardless of prompt.

3. **Implicit trigger threshold:** Prompts embedded in long, accumulated
   context don't activate skills as reliably as clean, isolated prompts.
   The noise-condition results from Experiment 001 (5 prior prompts) may
   underestimate the interference effect at real-world session scale
   (20-50+ prior exchanges).

4. **Model version drift:** Claude Code may serve different model versions
   across environments or across time. If the field environment is running a
   different version, activation behavior may differ independently of
   session conditions.

5. **Silent configuration failures:** Slug mismatches, permission gaps,
   or non-user-invocable flags can suppress activation without any
   visible error or acknowledgment from the model.

## How This Might Be Studied Further

**Compaction threshold test:** Run identical prompt sequences of increasing
length and measure at what session length skill activation begins to degrade.
If activation drops after a consistent number of exchanges, compaction is
the causal mechanism.

**Invocation marker audit:** After any skill-dependent output, verify the
presence of invocation markers rather than output structure alone. Structure
can be reproduced via file-read; the marker requires true invocation.

**Structured replication:** Run Experiment 001 conditions on the work
machine. Compare activation rates across identical conditions in both
environments. If the controlled environment is at ~100% and the field
environment is lower, the gap is the finding.

**Variable isolation:** Test each candidate explanation independently:
- Verify working directory before each run
- Control for session length and compaction state
- Log model version across runs

## Related Observations

- [Observation 007](007-silent-content-adaptation.md): Both involve the model
  doing something other than what was expected without disclosure. 007 is about
  content modification; 008 is about tool invocation failure.
- [Experiment 001](https://github.com/cgarciamx80/ai-eval-toolkit):
  The controlled dataset that makes the field-environment divergence visible.
  Without Experiment 001 as a baseline, the field-environment behavior would
  have no comparison point.

## Notes

This observation sits at the intersection of two disciplines:
LLM behavioral research and QA engineering. The environment-dependence
pattern is immediately legible to any QA professional who has seen a
test pass in staging and fail in production. The framing transfers.

The diagnostic prompt approach (asking the model to report on its own
skill environment after observing a skip) is itself a method worth
documenting. It produced specific, actionable hypotheses without requiring
access to internal model state.
