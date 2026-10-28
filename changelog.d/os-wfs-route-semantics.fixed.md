- Preserve WFS selection semantics in retrieval knowledge: a separate bounding-box
  parameter takes precedence over an attribute filter, so combined conditions
  belong in one XML filter. Record advertised property-value, stored-query and
  join capabilities separately from validated behaviour and native-field access.
  This extends the OS recovery record in issue #153 without admitting a new
  provider or executing source-supplied queries.
