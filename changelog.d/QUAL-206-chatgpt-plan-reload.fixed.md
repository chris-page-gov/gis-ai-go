- Fix the bounded ChatGPT tunnel pack so a prepared control plan accepts the
  repository's 40-character Git tree object identity when it is reloaded before
  connection. A regression rejects an incorrect 64-character SHA-256 substitution;
  no tunnel, provider, activation or deployment behaviour is widened.
