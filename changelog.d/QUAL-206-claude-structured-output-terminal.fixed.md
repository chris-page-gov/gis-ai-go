- Align the Claude exact-five terminal gate with Anthropic's structured-output
  result contract. Retain `end_turn` and accept `stop_reason: "tool_use"` only when
  the real CLI also reports `subtype: "success"`, a schema-valid
  `structured_output` and `terminal_reason: "completed"`, the process closes
  cleanly, and all five calls, contracts, receipts and the inspection relation pass
  independent verification. Keep incomplete tool-use runs fail-closed and require
  a new protected-main observation before publication.
