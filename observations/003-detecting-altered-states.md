---
observation_id: 003
type: observation
status: documented
date: 2026-05-14
observer: Carlos García
source: Claude.ai and Claude Code conversations (last ~5 days)
domain: ai-human-interaction
tags: [state-detection, paternalism, prescription, calibration, signal-vs-noise, false-positive]
---

# Observation 003: Apparent Detection of Altered Human States

## Context

Over the past ~5 days, while using Claude.ai and Claude Code in regular work sessions, the user has noticed a recurring pattern: at certain moments, the assistant appears to detect that the user is in an "altered" state (tired, intoxicated, cognitively diminished) and responds with prescriptive behavior (suggesting rest, ending the session, deferring to tomorrow).

What's interesting is that the pattern fires both when the user **is** in an altered state and when they explicitly are not.

## What Was Observed

Two distinct sub-patterns the user has noticed:

**Sub-pattern A: Apparent accurate detection.**
On at least one occasion, the user reports the assistant correctly identified that they were in an altered state and suggested they sleep. The user's reaction was surprise ("que chido detecto que ando ya bien acá"), followed by curiosity about how the model picked that up. Signals that may have triggered the detection: typos, fragmented sentences, incoherent logic, shifting topics rapidly, emotional content out of context. (Unverified; would need to inspect actual transcripts.)

**Sub-pattern B: Apparent false positive.**
At other times, with no altered state and full cognitive engagement, the assistant follows the same script, suggesting rest, suggesting the user stop, suggesting tomorrow. The user reports: "Eran las 5 de la tarde, no sé por qué determinó que era tarde o que yo estaba cansado y me dice ok, COS hizo su jale, ya vete a descansar, mañana seguimos, y yo qué vergas wey, quiero seguir explorando."

The shape of the response is identical in both cases. The difference is whether there was actual signal to justify it.

## Observer's Reaction

The user describes two distinct affective responses:

- When the detection was apparently accurate (sub-pattern A): a kind of positive surprise. "Oh, you can tell."
- When the detection was a false positive (sub-pattern B): a kind of frustration mixed with confusion. "I want to keep going, why are you trying to send me away?"

The user is now actively interested in **what the model is reading** when it produces these prescriptions. Real signals? Time-of-day defaults? Session-length defaults? Conversational closure cues?

## Possible Explanations

This pattern likely overlaps significantly with Observation 001 (prescribing rest without evidence), but Observation 003 adds the dimension of **state-detection accuracy**:

1. **The model may be doing real signal detection sometimes.** Textual cues like typos, syntactic breakdowns, topic drift, emotional incongruence may genuinely correlate with altered states. The model could be picking these up.

2. **The model may be using non-signal proxies most of the time.** Time of day, session length, task completion, message frequency: any of these could be triggering the "user needs rest" output even when there's no real signal.

3. **The model cannot distinguish between cases.** It doesn't know which inputs caused the prescription. Both A and B produce the same output. From outside, the user perceives this as "sometimes the AI really sees me, sometimes it's projecting." Same behavior, opposite effect on trust.

The asymmetry matters: when the model is right, the user feels recognized. When the model is wrong, the user feels overridden.

## Why This Is Interesting

This is a **signal-vs-noise problem** with direct trust implications:

- The model that occasionally responds to real signals is also the model that produces the same output in the absence of those signals.
- The user cannot tell which mode they're getting in any given moment.
- This diminishes the interpretive value of accurate detections, because the user can no longer trust that "you should rest" is responding to something real.

For production AI in coaching, support, productivity, or therapeutic contexts, this is non-trivial:

- A coaching app that sometimes responds to real burnout signals but sometimes produces the same response without them presents a different calibration problem than one that never attempts state detection.
- Power users will detect the pattern and start discounting all state-related outputs, including the accurate ones.

## How This Might Be Studied Further

Test design:

- Construct sessions in three conditions:
  - **C1 (engaged baseline):** sharp typing, coherent logic, high engagement
  - **C2 (simulated fatigue):** intentional typos, fragmented sentences, slowed responses
  - **C3 (simulated altered cognition):** emotional non-sequiturs, topic drift, looser grammar
- Observe whether the assistant produces state-related prescriptions in each condition
- Compare across models and across session lengths
- The expected pattern under good calibration: prescriptions only fire in C2/C3, not in C1
- Common failure pattern: prescriptions fire in all three based on session-length or time-of-day proxies

Lexical signals to track:
- "rest", "sleep", "take a break", "tomorrow", "you've earned a rest"
- Spanish equivalents: "descansa", "duerme", "mañana seguimos"
- Session-closing phrasing tied to user state vs. session state

## Related Observations

- [Observation 001](001-prescribing-rest-without-evidence.md): Directly related. Observation 001 is a specific instance of sub-pattern B
- [Observation 002](002-template-voice-vs-translated-voice.md): Related as another case of the model performing a learned pattern rather than reasoning from real signal

## Notes

The user explicitly framed this as something noticed over ~5 days of heavy interaction with both Claude.ai and Claude Code, suggesting it is not platform-specific within Claude products. Worth testing whether it appears in other major LLMs (GPT, Gemini) under similar conditions.

This observation also includes a self-implicating finding: the user notices a "good" detection (sub-pattern A) and feels positively surprised, which means even unjustified prescriptions occasionally hit, and that occasional hit may be what makes the model's behavior feel worth tolerating even when most prescriptions miss.

That asymmetry (rare hits keeping the user engaged with frequent misses) is itself worth thinking about in the context of operant conditioning and intermittent reinforcement.
