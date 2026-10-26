- Pace complete public-file verification to at most 50 request starts per second
  and retry only bounded transient HTTP failures, retaining every identity,
  file-length and digest check. Keep request, replay-byte and deadline ceilings,
  cancel error bodies unread and record actual retries in pass and failure
  evidence. Related to issue #153.
