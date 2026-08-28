- Preserve fail-closed ChatGPT exact-five evidence when the pinned tunnel client
  `v0.0.13` managed stop delivers `SIGTERM` a few milliseconds before or after
  observer stdin closes. The observer records `stdin-eof-and-sigterm` and
  `sigterm-then-stdin-eof` distinctly, allows at most 250 milliseconds for EOF
  after the signal, and still rejects a signal without EOF. Operating-system and
  application updates remain unsafe until the live observation has stopped and its
  private records have been persisted. Every call, receipt, runtime and publication
  gate remains unchanged.
