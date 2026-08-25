# QUAL-206 strict-modern evidence preparation

This preparatory compiler turns one private, closed host-capture summary into a
minimised public projection for the MCP `2026-07-28` target. It is additive to the
accepted QUAL-206 evidence. It does not upgrade or replace any earlier Claude,
Codex, ChatGPT or legacy result.

The compiler is deliberately capped below real-host capability acceptance. The
current telemetry wrapper is a summary source, not a versioned event-level
exact-five collector. A real capture can therefore be `not_ready` or
`ready_unscored`; only a clearly labelled synthetic fixture can exercise the
compiler's `capability_pass` state. All production, provider, registry, deployment,
release and completed-gate claims remain false.

## Trust boundaries

### 1. Private capture

The operator retains the manifest and telemetry locally in a directory with mode
`0700`; each input file must have mode `0600`, one hard link and current-user
ownership. The compiler opens each path through no-follow directory descriptors,
rejects symbolic links and hard links, bounds the bytes and checks that the file did
not change while it was read. Raw prompts, arguments, results, headers, environment
values, session identifiers and compiler-owned outcome fields are not accepted in
the manifest.

The raw telemetry is checked against the private digest and byte count in the
manifest, but neither value is published. This avoids turning a retained private
transcript into a linkable public identifier or a brute-force oracle.

### 2. Compiler

The compiler validates the closed capture schema, derives the status and negative
claims, applies the public privacy allowlist and validates the closed public schema.
It binds its own source, both schemas and the shared canonical-identity source and
built runtime. The compiler rejects drift from the reviewed hashes of the three
generated identity-runtime files. The output identity uses the repository's RFC
8785 implementation and the domain
`gis-ai-go.qual-206-strict-modern-host-evidence.v2`.

For an observed-host summary, the source inventory is exact rather than
caller-selectable. Tracked inputs are compared with the stated commit through
`git show`; generated identity runtime files are compared byte-for-byte with the
recorded digests. The commit must be an ancestor of the local `origin/main` ref.
This is a source-binding check, not independent proof that the remote protected
branch or the host process used those bytes.

### 3. Public projection

The projection contains fixed classifications, bounded counters, allowlisted host
and protocol metadata, source digests, derived outcomes and explicit limitations.
It contains no raw telemetry path or content, raw telemetry digest or byte count,
request identifier, prompt, result, credential, hostname, username or arbitrary
operator prose. Output creation is exclusive: an existing evidence file is never
overwritten.

## Claim-to-source matrix

| Public field or claim | Source | Current assurance |
| --- | --- | --- |
| Capture classification and time | Closed private manifest | Schema-valid summary |
| Protocol and readiness outcome | Compiler derivation from bounded observation fields and closed counters | Summary-level only |
| Exact-five capability | Synthetic fixture only | Cannot become a real-host claim |
| Source commit, tree and material digests | Git objects plus local generated identity runtime | Source-bound; local `origin/main` ancestry only |
| Compiler and schema identity | Compiler-read source and built files | Bound into the RFC 8785 evidence identity |
| Private telemetry | Owner-controlled local file | Content, path, digest and byte count withheld |
| Live provider, remote HTTP and production lifecycle claims | Compiler constants | Always false in this contract |
| Earlier Claude and base-corpus evidence | Fixed additive lineage hashes | `preserved-separate-not-superseded` |

## Run the compiler

Build the shared evidence package first, then compile into a new output path:

```bash
pnpm --filter @gis-ai-go/evidence run build
uv run --locked --cache-dir .uv-cache python \
  scripts/compile_qual_206_strict_modern_evidence.py \
  --capture-root PRIVATE_CAPTURE_ROOT \
  --capture capture.json \
  --output NEW_PUBLIC_EVIDENCE.json
```

`PRIVATE_CAPTURE_ROOT` must be an absolute owner-only directory. The command fails
if the output already exists. Keep the private input outside the repository and do
not commit it.

## Remaining acceptance work

A versioned event-level collector must independently validate one complete session:
the exact opening sequence, request and response pairing, unique identifiers,
allowed methods, exact-five operations, resources, cancellation, unsupported
traffic, close, process exit and stderr. It must bind the actual host executable and
deterministic runtime build. Only that later collector and compiler can support a
real-host capability result.

Separate governed evidence is still required for remote HTTP, a live provider,
public runtime identity and TLS, storage and recovery, operations, deployment,
registry publication, activation and release.
