# Geospatial execution boundary

This Python workspace records the deterministic execution-service boundary. Stage 0
contains no geospatial library, provider adapter or network transport. Calling
`execute` always raises `StageZeroBoundaryError`.
