# Reference design — Functional scope

This is an author-written answer to [the assignment](README.md#assignment), not your study
evidence. Read it before a guided attempt or compare afterwards. Your own response belongs
in [DESIGN.md](DESIGN.md). This is one defensible scope under the assumptions below.

## Assumptions and requirement

The product is a link-shortening service: a creator stores a destination and receives a short
link that visitors can open. Assume a trusted owner identity is available for management
actions; designing authentication is outside this first scope exercise. Only supported web
destinations are accepted. Destination content and uptime are controlled by another service.

The task requires three user actions, two exclusions, and one measurable success criterion.
The decisions below are proposed requirements, not claims about an implemented service.

## Three user actions

| Actor and action | Input | Observable result | Failure behavior |
| --- | --- | --- | --- |
| Creator creates a short link | A supported destination URL | Receives a short URL after the mapping is stored successfully | Invalid input is rejected; a failed save is not reported as success |
| Visitor opens a short link | A short code | Receives a redirect to that code's saved destination when active | Unknown or disabled codes return an unavailable-link response, not an unrelated destination |
| Owner disables a link | A code belonging to that owner | Receives confirmation that the mapping is disabled | An unauthorized caller cannot change it; a failed update is reported explicitly |

Disabling affects new resolutions after the state becomes visible. It cannot retract a
redirect already delivered to a browser. The exact visibility delay is a quality requirement
to specify in [Day 2](../../day-002-find-the-first-maximum/sd_quality-requirements/REFERENCE_DESIGN.md).

## Two exclusions

1. **No custom aliases in this version.** The service chooses codes; creators do not reserve
   branded words. This avoids adding alias ownership and naming-conflict behavior to the scope.
2. **No click analytics in this version.** Counting visitors and reporting dashboards are not
   promised. Opening a link does not depend on recording an analytics event.

These are deliberate product boundaries, not assertions that the features are technically impossible.

## Diagram and measurable criterion

```text
creator -> shortener -> save code/destination/status -> return short URL
visitor -> shortener -> look up active code -> redirect response
visitor's browser -> destination service
owner -> shortener -> authorize ownership -> mark code disabled
```

The proposed functional acceptance criterion is: in a controlled fixture of **100 distinct,
known active mappings**, every resolution returns that mapping's exact saved destination,
with **zero cross-mapping results**. The fixture size and perfect-match threshold are assumed
acceptance choices, not measured production reliability. Inspect the shortener's response;
the destination site's availability is outside this boundary. No test run is claimed here.

Additionally, a create-then-resolve scenario checks that the returned code actually identifies
the newly saved destination. A disable scenario checks the agreed visibility rule once that
rule is defined. These cases expose omissions that a redirect-only fixture cannot cover.

## Decision and alternative

Choose the smallest lifecycle with creation, resolution, and disabling. Disabling gives an
owner a way to withdraw a link without requiring permanent record deletion in the first scope.
An alternative is to offer creation and resolution only, using destination lookup as the third
action. That is simpler but gives owners less control. A requirement to withdraw mistaken
or obsolete links favors the proposed lifecycle; lack of ownership support would require revisiting it.

## Failure walkthrough

Suppose saving a new mapping fails, but the service still returns a short URL. The creator
shares it and visitors cannot resolve it. This breaks the promise that successful creation
produces a stored mapping. Return success only after the save succeeds. If the save succeeded
but the response was lost, the creator sees uncertainty: a retry might create another code.
That ambiguity should be recorded for later idempotency design, not hidden behind a success claim.

## Self-review

The scope is complete enough to discuss behavior, but ownership, destination validation,
disabled-link visibility, and retry semantics need further decisions. Next, define measurable
quality targets and verify the create/resolve/disable scenarios against a future implementation.
This document completes the reference answer; it does not establish learner mastery or test results.

[Concept explanation](CONCEPTS.md) · [Your practice](DESIGN.md) · [Navigation](README.md)
