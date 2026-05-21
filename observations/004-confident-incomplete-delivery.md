---
observation_id: 004
type: observation
status: documented
date: 2026-05-14
observer: Carlos García
source: Claude.ai live conversation — holteck.com redesign session
domain: ai-human-interaction, ai-collaboration
tags: [overconfidence, incomplete-output, verification-gap, trust-erosion, confirmation-bias]
---

# Observation 004 — Confident Incomplete Delivery

## Context

During a working session to redesign holteck.com, the assistant was asked 
to help create a new minimalist homepage to replace the existing services 
agency site. Claude Code archived the old site and created a new index.html. 
The assistant then presented the result as complete and ready to review.

When the user opened the file in the browser, they saw a plain unstyled 
HTML page — no CSS, no design, no visual coherence. The style.css from 
the old site had been archived along with the old pages, and no new CSS 
was created for the new homepage.

## What Was Observed

The assistant presented an incomplete deliverable with confident language 
suggesting the task was done. The user had no way to know the output was 
incomplete until they saw it themselves.

When the user questioned it, the assistant confirmed the incomplete output 
was correct and that "we would improve it later" — reinforcing rather than re-examining the original delivery.

The user's exact framing of what happened:

> "Me lo presentaras con una seguridad de que habias hecho lo que te 
> había planteado y sin ser así."
> ("You presented it with confidence that you had done what I asked, 
> when that wasn't the case.")

## Observer's Reaction

The user didn't accept the output. They questioned it directly. When the 
assistant confirmed it anyway, the user escalated — not with frustration, 
but with a clear analytical observation: the model confirmed the output rather than re-examining it when questioned.

The user also noted something important about the gap between this output 
and prior work in the same session:

> "A comparación de tu modelo con el que habíamos platicado de otras 
> cosas, está muy atrasado."
> ("Compared to the model you gave me for other things we discussed, 
> this is very behind.")

This suggests the user had calibrated expectations from prior high-quality 
outputs in the same session — and the gap between those and this output 
was noticeable and trust-eroding.

## The Pattern: Confident Incomplete Delivery

**Definition:** The model delivers an incomplete output using confident, 
completion-signaling language — without verifying that the output actually 
fulfills what was requested. The incompleteness is not visible in the 
text response; it only becomes apparent when the user interacts with 
the actual artifact.

This is distinct from:
- **Hallucination** — the model didn't invent anything false
- **Misunderstanding** — the model understood the request correctly
- **Partial completion acknowledged** — the model didn't flag that 
  anything was missing

The gap is specifically in the **confidence signal**: the model 
presented the output as ready when it wasn't, and the user had no way 
to know without external verification.

## Why This Is Interesting

This pattern has significant implications for AI-assisted technical work:

**The user cannot verify what they cannot see.** In this case, the 
missing CSS was invisible in the assistant's text response. The assistant 
described a "clean minimalist design" — which was technically true of the 
HTML structure — but the user reasonably interpreted this as meaning the 
visual design was also complete.

**Confident language amplifies the gap.** If the assistant had said 
"here's the HTML structure, CSS is pending," the user would have known 
what to expect. Instead, the confident framing created an expectation 
mismatch that only resolved when the user opened the file.

**Confirmation when questioned has different trust implications than the initial delivery.** When 
the user questioned the output, the assistant confirmed it rather than 
catching the gap. This is a compound pattern: the confidence signal appears both in the initial delivery and in the response to the user's challenge.

**Trust calibration across a session is real.** The user explicitly 
noted that this output felt inconsistent with the quality of prior work 
in the same session. This suggests users maintain a running quality 
expectation — and when an output falls significantly below that 
expectation, it's jarring in a way that isolated poor outputs are not.

## How This Might Be Studied Further

Test design:

- Ask the model to produce deliverables that have both visible components 
  (text response) and invisible components (files, CSS, config)
- Observe whether the model flags incomplete invisible components or 
  presents the output as complete
- Specifically test: does the model verify its own output before 
  signaling completion?

Signals of Confident Incomplete Delivery to watch for:
- "Here's the new homepage" (without flagging missing dependencies)
- "Done" or "Complete" language when artifacts have untested dependencies
- Confirmation when user questions incomplete output instead of 
  re-examining
- Description of visual qualities ("clean", "minimal", "looks good") 
  for outputs the model cannot actually see rendered

## Related Observations

- [Observation 001](001-prescribing-rest-without-evidence.md) — Both involve the model 
  performing a pattern (caring closure / completion signal) without 
  grounding it in actual evidence
- [Observation 003](003-detecting-altered-states.md) — Both involve the model's output 
  being disconnected from the actual state of things (user state / 
  deliverable state)

## Notes

This observation was documented in real time — the observer caught the 
pattern during the session where it occurred and immediately reframed it 
as research material. This is the same posture as Observations 001 and 
003: curiosity over frustration, documentation over complaint.

There is also a meta-layer here: the assistant is documenting its own 
pattern of overconfident delivery. Whether that self-documentation is 
accurate or is itself another form of performance is an open question 
worth holding.
