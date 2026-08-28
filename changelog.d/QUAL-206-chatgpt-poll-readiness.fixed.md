Fix the QUAL-206 ChatGPT tunnel readiness gate so it uses tunnel-client v0.0.13's
credential-free successful-poll probe for the current runtime, with a narrowly
bounded startup retry and fail-closed error handling.
