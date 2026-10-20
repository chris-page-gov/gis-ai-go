# Bounded local GML processing candidate

Owner: repository owner. Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Method version: 1, authored 20 October 2026. This is a provider-free maintenance
candidate; canonical source assurance remains separate from local verification.

The local recovery needs to inspect complete selected GML inputs without
retaining feature values in its knowledge files. `gml_profile.py` performs a
bounded complete XML traversal; `gml_archive_profile.py` admits one checksum-bound
ZIP or gzip selection, processes every XML member and verifies retained evidence.
Neither method fetches data, executes archive contents, converts formats or
disposes of raw payloads. No new hosted tool or provider is admitted.

## Policy and threat boundary

Inputs are untrusted bytes. Threats include archive traversal, links and special
files, case/Unicode collisions, decompression bombs, XML DTD/entity expansion,
credential leakage, overwrite races, source substitution and false completeness.
Use a private directory on the verified local filesystem and a bounded process.
Never publish licensed inputs, private selection descriptors or machine paths.

ZIP admission checks every central-directory entry before extraction: path
components, duplicates, file types, encryption, implicit-directory conflicts and
case/Unicode-normalisation collisions. Extraction uses new flat filenames,
exclusive creation and no symbolic links. ZIP CRC and gzip trailers must pass.
One gzip layer inside ZIP is supported; deeper containers are refused. A non-XML
member blocks completion unless its exact path and checksum are explicitly
classified as bounded UTF-8 documentation or schema, retained and verified.

XML rejects DTDs, entity declarations and external entities. It never fetches XSD
imports or resolves XLinks. Native QNames/EQName XPath, repeated order, attributes,
nil/empty/text/absence states, root schema locations and selected CRS/unit metadata
remain source evidence. Coordinates, feature identifiers and ordinary field
values are redacted. The exact legacy `osgb:BNG` CRS label is retained as an opaque
source identifier; no EPSG equivalence or general URI-scheme admission is inferred.
Comments, processing instructions and lexical XML are not
retained; raw sources therefore remain necessary evidence.

## Evidence and limits

Each native element/attribute has a directly readable JSON-LD field card linked
to the complete source digest and selected mode/version evidence. All files,
including cards and manifests, are at most 16 KiB. Large field details reconstruct
losslessly through checksummed per-field parts. Structural patterns are linked by
digest. An index supports exact native-path discovery. Missing version evidence
remains unestablished, and matching names do not imply cross-format equivalence.

The XML defaults are 64 MiB input, depth 128, one million elements, two million
attributes, 20,000 distinct paths, 20,000 order items per element and 32 MiB
measured structural metadata. Order items include child elements and intervening
text or whitespace. Archive
defaults are 256 MiB raw/expanded, 128 MiB per member, 10,000 members including
nested expansions and 600 seconds cooperative wall time. Both gzip-container
bytes and decoded bytes count. Each XML member receives the remaining archive
wall budget; an outer process deadline remains necessary for a hard deadline.
The archive CLI accepts an explicit positive `--max-sequence-items` bound while
keeping the 20,000 default. Record an input-specific structural count and memory
assessment before increasing it. The chosen value is retained in archive and XML
profiles; exceeding it fails the complete scan and preserves its inputs.

Outputs use fresh private directories and exclusive writes. A candidate bundle
is fully verified before its completion marker is published without replacement.
Interrupted directories remain explicit; they are not reused. This establishes
software checks and file/directory synchronisation, not hardware power-loss
durability. The archive completion marker follows verification of every member,
profile, field card and the original payload's final checksum.

An independent ElementTree pass counts common GML membership wrappers and a
limited named set of OS feature elements. Total element counts must agree with
the primary Expat traversal. Feature counts remain candidate membership counts:
unresolved XLinks, FULL/COU baseline application and removed-feature semantics
are not established. Exact `insert`, `replace` and `delete` children of the OS
product 1.0 `Transaction` root have separate action counts and direct child QName
counts. These candidate action children are not added to generic feature counts.
Empty actions, referenced features and deletion effects remain unresolved; a zero
generic membership count does not prove that a transaction contains no features.

## Descriptor and output contract

The [closed JSON Schema](../../okf-plus/schemas/gml-local-processing.schema.json)
covers the acquisition descriptor and archive completion record. Runtime
verification additionally binds the raw size/SHA-256, optional MD5, source
selection digest and JSON pointer. Native delivery labels remain unchanged;
normalisations to FULL/COU are explicitly source-label candidates. Contract
validity does not prove upstream truth or permit execution.

The descriptor contains `payload` (`bytes`, `sha256`, optional `file`/`md5`),
`selection` (`id`, `deliveryMode`) and `selectionEvidence` (`file`, `sha256`,
`jsonPointer`). The latter must resolve to the same selected ID/mode. Optional
`classifications` contain exact `path`, `kind` and `sha256` for retained text.

Completion explicitly fixes `conversionSuccess`, `rawPayloadDisposed` and
`schemaMappingComplete` to false. Complete structural processing of one archive
does not establish schema closure, mapping completeness, full PSGA coverage or
successful conversion. Retain raw inputs until a separately reviewed complete
semantic/disposal procedure establishes that the required knowledge survives.

## Run and verify

Use the locked development environment and a tested Linux filesystem:

```sh
uv run --locked --cache-dir .uv-cache python -m scripts.okf_plus.gml_archive_profile \
  --receipt artifacts/private-input/descriptor.json \
  --payload artifacts/private-input/selected.gz \
  --work-dir artifacts/private-transient/new-run \
  --output artifacts/private-knowledge/new-run
```

The two destination parents must exist and the destinations must be new.
No symbolic-link ancestor is admitted. A failure preserves original and
transient payloads and records a non-reflective private failure. There is no
automatic retry, acquisition, deletion, support submission or publication.

The synthetic suites `test_okf_plus_gml_profile`,
`test_okf_plus_gml_archive_profile` and `test_okf_plus_gml_contracts` check
complete traversal, value redaction, field-card lookup/reconstruction, namespace
paths, bounds, ZIP/gzip corruption, unsafe archives, source binding, no-overwrite,
interrupted publication and refusals of false disposal/conversion assertions.
Current-schema XPath and other-format semantic mappings remain separate work.
