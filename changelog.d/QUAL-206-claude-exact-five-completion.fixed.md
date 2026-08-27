- Give the bounded Claude exact-five profile one additional agentic turn after two
  private observations stopped before `evidence.inspect`, require an `end_turn`
  terminal result, and make the model wait for the fifth response and copy its
  distinct receipt rather than substitute the search receipt for it. Normalise
  nested composite verification failures to the exact-five verifier's error
  contract and bind reported total turns to the documented ceiling rather than an
  assumed exact count.
