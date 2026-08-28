- Preserve fail-closed ChatGPT exact-five evidence when the pinned tunnel client
  closes observer stdin and immediately sends `SIGTERM`. The observer now gives the
  already-requested EOF a bounded 250-millisecond delivery grace, still rejects a
  signal without EOF and leaves every call, receipt, runtime and publication gate
  unchanged.
