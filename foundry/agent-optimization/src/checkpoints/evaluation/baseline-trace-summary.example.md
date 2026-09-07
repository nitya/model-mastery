# Instructor-prepared trace example

> **Not live telemetry:** these illustrative values exist only so learners can
> practise reading a span breakdown when trace export is unavailable.

| Span | Duration (illustrative) | Input tokens | Output tokens |
|---|---:|---:|---:|
| `product-launch-studio` | 8.4 s | — | — |
| `campaign-coordinator` | 0.9 s | 620 | 105 |
| `visual-understanding` | 2.1 s | 890 | 180 |
| `campaign-reasoning` | 2.4 s | 760 | 250 |
| `adaptive-copy` | 3.0 s | 1,240 | 510 |

Example hypothesis: the fixed `adaptive-copy` call spends the largest share of
the request on a heavily constrained prompt, so routing is worth evaluating
against the frozen dataset. This is a hypothesis, not a measured conclusion.
