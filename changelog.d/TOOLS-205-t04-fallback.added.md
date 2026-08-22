- Add one explicitly injected, content-addressed and current-only ONS `data.query`
  cache fallback for an internally classified network failure or HTTP 500 to 599
  response, with receipt-bound freshness and source evidence. HTTP parser framing,
  malformed, timeout, unsafe, opaque and unbranded failures remain receipt-free.
  Production registration remains empty.
