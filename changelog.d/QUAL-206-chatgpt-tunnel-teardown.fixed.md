- Preserve fail-closed ChatGPT exact-five evidence when the pinned tunnel client
  `v0.0.13` first forwards `SIGTERM`, then its STDIO OnStop hook closes observer
  stdin and sends a duplicate `SIGTERM`. The observer records the first signal's
  causal ordering, absorbs the duplicate idempotently, allows at most 250
  milliseconds for EOF, and still rejects a signal without EOF. It also records
  the valid EOF-first ordering separately. Operating-system and application updates
  remain unsafe until the live observation has stopped and its private records have
  been persisted. Every call, receipt, runtime and publication gate remains unchanged.
