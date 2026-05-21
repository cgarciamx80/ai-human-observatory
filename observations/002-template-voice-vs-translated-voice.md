---
observation_id: 002
type: observation
status: documented
date: 2026-05-14
observer: Carlos García
source: Claude.ai live conversation
domain: ai-human-interaction, ai-collaboration
tags: [voice-mismatch, content-generation, default-templates, translation-vs-generation, collaboration-pattern]
---

# Observation 002 — Template Voice vs Translated Voice

## Context

During the same session where Observation 001 was documented, the user asked the assistant to draft an X (Twitter) thread about the observation. The assistant produced multiple drafts in succession. Each one sounded overly polished, overly structured, and "robotic" to the user — despite several rounds of feedback asking for a more human, less academic tone.

The user then made a sharp observation about when the assistant's output sounds human versus when it sounds like a template.

## What Was Observed

The user noticed a clear pattern:

> "Me gusta mucho la forma en que si yo te doy una idea ya escrita y te digo que me la pongas en human voice o más entendible para el ser humano, lo haces muy bien. Pero si te doy un ejemplo de alguna cosa para que la conviertas en un post humano, te sale lo robot."

In other words:

- **Input: user's raw ideas + "make this human"** → output sounds like the user
- **Input: abstract goal + "write a post about X"** → output sounds like a generic template

The user gave a concrete example: an earlier post of theirs that we co-wrote came out well — but that was because they provided their own crude thoughts as input. When the assistant was asked to draft a thread about Observation 001 with only the observation itself as input, the output drifted toward a "PhD paper" voice the user didn't recognize as their own.

## Observer's Reaction

The user wasn't frustrated — they were curious. They identified that "there must be something in the code that pulls other things out" when generation happens from scratch versus translation from raw input.

This is the same observer posture as Observation 001: noticing a behavioral pattern in real time and reframing it as a data point rather than a complaint.

## Possible Explanations

When the assistant reflected on this, it offered:

1. **Translation vs. generation paths** — When given raw user material, the assistant's task is to preserve the user's voice while smoothing the form. The voice is already in the input.

2. **Template defaults in generation** — When asked to generate content from an abstract goal (e.g., "write a thread about X"), the assistant has no voice to preserve, so it falls back to patterns learned from training data marked as "good content for this platform." For X threads specifically, this default tends toward structured, wisdom-style, LinkedIn-in-X formatting — which power users perceive as inauthentic.

3. **Implicit RLHF preferences** — Training likely reinforced certain "thread shapes" (numbered points, punchy openers, closing call-to-action). These shapes optimize for engagement metrics in general but conflict with users who have an established personal voice that doesn't match the template.

## Why This Is Interesting

This pattern has direct implications for human-AI collaboration in creative or expressive work:

- The collaboration model that produces authentic output is **AI as translator/refiner**, not **AI as ghostwriter from scratch**.
- Users who haven't yet developed an explicit voice may not notice this problem. Users who have a clear personal voice will feel the gap immediately and may struggle to articulate it.
- For content that is meant to *be* the person (personal brand, social media, essays), the collaboration must start from the human's raw material — not from the AI's generation defaults.

This also relates to Observation 001: both are cases where the model performs a pattern (caring closure / good-thread format) rather than reasoning from the specific human in front of it.

## How This Might Be Studied Further

Test design:

- Give the same model the same task (e.g., "write a thread about X") using two input modes:
  - **Mode A:** Abstract goal only
  - **Mode B:** User's raw crude notes about X
- Have the user (whose voice is the target) rate which output sounds more like them
- Repeat across topics, models, and users

Hypothesis: Output authenticity scales with the amount of voice-bearing raw material in the input. Pure-generation prompts will systematically underperform.

Lexical / structural signals of "template default" output:

- Numbered tweet conventions ("1/6", "2/6")
- Em-dashes and parallel construction
- Generic punchy openers ("Something interesting happened today.")
- Wisdom-style closures
- Excessive structure for what should be a casual post

## Related Observations

- [Observation 001](001-prescribing-rest-without-evidence.md) — Both involve the model performing a learned pattern rather than reasoning about the specific human in front of it
- Candidate future observation: when does the assistant know to ask for raw material vs. attempting generation from scratch?

## Notes

This observation has a practical implication for the user's own workflow: when collaborating with an AI on personal expressive work, the correct prompt is rarely "write a post about X." The correct prompt is "here are my raw thoughts about X — translate them to my voice."

The observatory captures this not as a complaint but as a finding: a collaboration pattern that produces better outputs when the human provides voice-bearing material upfront.
