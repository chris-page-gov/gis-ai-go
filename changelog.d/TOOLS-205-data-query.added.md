Added an inactive transport-neutral `data.query` application for the exact reviewed
ONS version 121 single-observation resource. It requires explicit adapter injection,
keeps discovery and invocation lifecycle planes independent, verifies policy,
limits, rights, provenance and results before producing fully checked v2 evidence,
attributes caller cancellation and caller deadline expiry separately from a
provider-local timeout, and exposes no route, MCP tool, activation override or
deployment.
