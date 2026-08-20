# ADR-0008: Supported Pages transport from verified payload

- status: accepted
- decided on: 20 August 2026
- work item: DISC-104
- supersedes: ADR-0007 deployment transport step 4

## Context

ADR-0007 deliberately separated the attested publication archive from deployment
authority. Four dispatches verified the selected source run, commit, archive digest,
receipt, provenance and Pages configuration, then failed closed during GitHub Pages
ingestion. The fourth run proved that the exact corrected POSIX ustar reached Pages
with `./` paths, non-root ownership, regular files only and no links or special
members. GitHub still returned only `deployment_failed`.

GitHub identifies its pinned `actions/upload-pages-artifact` action as the Pages
packaging implementation reference. That action creates a native GNU tar from a
directory before uploading the current-run `github-pages` artefact. Continuing to
guess undocumented tar-header details would weaken the evidence boundary without
providing a supported result.

## Decision

Retain three distinct and explicitly named layers:

1. **Attested source archive** — protected-main CI builds the deterministic
   `artifact.tar`, checksum and receipt once. The exact tar digest is retained and
   attested as `pages-source-<source-commit>`.
2. **Verified logical payload** — the manual workflow revalidates the source run,
   archive, receipt and GitHub provenance, then safely materialises its already
   verified regular files into a new empty directory. It rejects traversal, links,
   special files, pre-existing output and any inventory or byte mismatch.
3. **GitHub Pages transport** — the same successful prepare job passes only that
   verified directory to the exact commit-pinned official
   `actions/upload-pages-artifact` action, including the two allowlisted hidden
   files. GitHub creates the platform transport tar. The protected deploy job only
   configures Pages and deploys that current-run artefact.

The workflow must not run the Explorer build, edit a publication file or treat the
platform tar as the attested source archive. The dispatch `archive_sha256` remains
the SHA-256 of the retained source archive. Public verification must still fetch and
hash the complete served payload and supporting publication metadata against roots
and digests from the independently verified source receipt.

Rollback and restore select retained accepted source archives. They rematerialise
the exact same logical publication bytes and create a new supported platform
transport envelope; they do not rebuild the product. Therefore, the Pages transport
tar digest may differ between deployments while the selected source archive digest,
payload root, publication checksums, source commit and product version remain exact.

If the exact pinned official transport also fails ingestion, stop changing archive
formats and escalate the recorded run, deployment and artefact identities to GitHub
Support.

## Consequences

- the public URL remains traceable to one attested source archive and its complete
  verified logical payload;
- the workflow describes the platform tar as a transport envelope, not immutable
  product evidence;
- upload happens only after all source gates pass and before the separate
  least-privilege deployment job;
- allowlisted hidden files are retained without exposing `.git`, `.github` or any
  unverified file;
- public verification remains the final proof that GitHub served the selected
  accepted bytes; and
- ADR-0007's build, attestation, selection, security and rollback principles remain
  accepted except for its unchanged-tar transport claim.
