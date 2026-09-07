# Instructor-prepared optimizer review example

> **Not a live optimizer result:** this document contains illustrative teaching
> values. It has no service operation ID or valid candidate ID. Prefer the
> learner's live Agent Optimizer output whenever available.

Compare:

- `checkpoints/00-baseline/instructions.md`
- `checkpoints/01-evidence-optimized/instructions.md`
- `checkpoints/optimizer-result.sample.json`

| Configuration | Overall | Evidence fidelity | Task adherence |
|---|---:|---:|---:|
| Baseline example | 0.70 | 0.88 | 0.52 |
| Evidence-optimized example | 0.84 | 0.94 | 0.81 |

The prepared candidate adds evidence mapping, qualifier preservation, safe
recovery for unsupported claims, and explicit output checks. The example shows
the intended review method: reject any candidate that improves aggregate score
while weakening grounding. Do not pass `prepared-evidence-optimized` to
`azd ai agent optimize apply`; it is a local label, not a live candidate ID.
