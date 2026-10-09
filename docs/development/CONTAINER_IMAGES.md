# Select and admit container images

Status: options researched on 9 October 2026; no vendor image, subscription,
internal mirror or secure-platform admission is selected by this document.
The [actual image scans](BUILD_ASSURANCE.md) currently block both tested images.
Vendor descriptions are not scan results for the GIS AI GO image. The platform
must review the exact digest, architecture, complete dependency closure,
vulnerabilities/VEX, SBOM, provenance/signatures, tool compatibility and update
owner before secure use.

Keep three purposes separate: an editor/development image needs Bash, Git and the
pinned toolchain; an approved builder needs controlled dependency/image access;
the Cloud Run image needs only the application runtime and admitted outputs.
Adding build tools to a runtime image changes its contents and assurance. The
current additive Debian/Node GCP application image does not inherit the earlier
UBI candidate's acceptance or a vendor's hardened-image claims.

## Verified options

| Option | Official documented properties | Work still required here |
| --- | --- | --- |
| Repository development image | Explicit digest-pinned Node/Python bases and staged, hash-bound tooling; a separate development image | Full image build/scan/SBOM/provenance and source/platform review; confirm exact tool versions, permissions, browser/caches and architecture. It is not branded as a Docker Hardened Image. |
| Docker Hardened Images (DHI) | Docker distinguishes `-dev` variants with shell/package/build tools from minimal runtime variants; signed attestations and separate Community/Select/Enterprise facilities | Verify available exact versions, libraries/CA, permitted registry/authentication and subscription/mirroring rights; evaluate a combined approved developer toolchain without inheriting runtime claims. |
| Chainguard Containers | Minimal runtime and `-dev` variants, signed images/attestations; public Free images limited to latest/latest-dev, with separate Production versioned access | Verify entitlement for the pinned versions, expected public/private signing identity, approved internal mirror and complete tool/runtime compatibility. No subscription or external registry is assumed. |
| Google Distroless | Application/runtime dependencies without a normal shell or package manager; Node.js 24 and nonroot/debug variants are listed; keyless Cosign verification documented | Candidate runtime migration, not a drop-in editor image. Verify exact digest, architecture, runtime entrypoint, CA/native-library compatibility and complete child-image scan/provenance. |

### Docker Hardened Images

Docker's official documentation describes Community core images as free and
Apache 2.0, with registry authentication to `dhi.io`. This is a vendor availability
statement, not authorisation to create a Docker account, accept terms or introduce
an external registry on the secure machine. Docker's managed mirroring and
customisation/compliance/SLA facilities have subscription and organisation
requirements; the platform supplies the actual approved entitlement and mirror.

Docker documents image layers and signed attestations at separate registry
locations, including `registry.scout.docker.com`. A copied image alone may not
preserve its attestations. Validate the exact architecture's upstream signatures,
SBOM/provenance and any admitted VEX, then retain equivalent evidence through the
approved internal mirror. Adding this repository's toolchain/application layers
requires child-image assurance. Docker's scan guide calls for maximum provenance
and SBOM so its scanner can establish DHI base lineage; those flags do not by
themselves verify the builder, approve findings or prove a secure child image.

The official quickstart's pull/login/build examples are vendor documentation, not
instructions to run before this repository's source/image/platform gates. No DHI
pull, authentication, image scan or entitlement was observed by this research.

Sources read from Docker's official documentation repository on 9 October:

- [DHI overview source](https://github.com/docker/docs/blob/main/content/manuals/dhi/_index.md)
- [Development/runtime considerations](https://github.com/docker/docs/blob/main/content/manuals/dhi/how-to/use.md)
- [Mirroring requirements](https://github.com/docker/docs/blob/main/content/manuals/dhi/how-to/mirror.md)
- [Signed attestation verification](https://github.com/docker/docs/blob/main/content/manuals/dhi/how-to/verify.md)
- [Image scanning and child-image lineage](https://github.com/docker/docs/blob/main/content/manuals/dhi/how-to/scan.md)
- [Select/Enterprise prerequisites](https://github.com/docker/docs/blob/main/content/manuals/dhi/how-to/select-enterprise.md)

### Chainguard Containers

Chainguard's official overview distinguishes minimal runtime images from `-dev`
variants that include development utilities. It describes signed images,
build-time SBOMs and nightly rebuilds. These are vendor properties; the completed
repository child image still needs its own scan, dependency/SBOM/provenance
review, update decision and platform admission.

The public build repository describes per-architecture `locked_config.json`
files and a release pipeline publishing SBOMs/Cosign attestations with each image.
Use the selected image's real lock/provenance identity as evidence; a link to that
repository does not prove the bytes in a chosen internal mirror or child image.

The overview limits public Free images to `latest` and `latest-dev`. Production
access provides versioned variants and additional commercial facilities. Resolve
and approve an immutable digest, then check whether the exact pinned Node/Python
and other tooling versions are actually available under the platform's
entitlement. A public latest image does not establish that older pinned versions,
production SLA or custom assembly are available. No paid subscription is
authorised by this options review.

The signature guide distinguishes public GitHub-based signing identities from
the organisation's private image-sync/custom-builder identities and issuers.
The platform must validate the correct expected issuer/identity and retain
signature/attestation evidence through its approved mirror. Do not apply a public
image's verification policy blindly to a private/customised one. No Chainguard
image pull, vendor login, licence entitlement or scan was observed here.

Sources read from Chainguard's official documentation repository on 9 October:

- [Public image build configuration and release pipeline](https://github.com/chainguard-images/images/blob/main/README.md)
- [Container overview and Free/Production availability](https://github.com/chainguard-dev/edu/blob/main/content/chainguard/containers/overview.md)
- [Catalog pricing and entitlement model](https://github.com/chainguard-dev/edu/blob/main/content/chainguard/containers/reference/pricing/index.md)
- [Registry access](https://github.com/chainguard-dev/edu/blob/main/content/chainguard/containers/registry/overview.md)
- [Image and attestation signature verification](https://github.com/chainguard-dev/edu/blob/main/content/chainguard/containers/security-and-compliance/verifying-chainguard-images-and-metadata-signatures-with-cosign/index.md)

### Google Distroless

The official project says normal distroless images have no shell/package manager.
Its Node.js runtime variants use a language-specific entrypoint; Docker command
and entrypoint forms need review. Debug variants deliberately add shell access
and have different contents. Select non-root behaviour explicitly and verify it,
rather than assuming every variant has the same user or tool surface.

The project documents keyless Cosign signatures with the Google issuer and its
named signing identity. The platform must verify that exact expected identity and
digest through its approved trust route; a registry name, a digest alone or an
unverified copied signature is insufficient. No distroless image was pulled or
tested for this deployment by this research.

- [Official project README, supported variants and signature verification](https://github.com/GoogleContainerTools/distroless/blob/main/README.md)

The source response dates and SHA-256 hashes are retained locally in
`artifacts/security/gcp-223/vendor-sources/observations.json`. Upstream `main`
links are mutable; the platform must bind its chosen image/source/provenance
identities rather than treating those links as immutable admission evidence.

## Platform decision and execution

Record the exact internal image digest, registry, architecture, allowed tools,
source commit, scan and SBOM/provenance/signature results, unresolved findings,
expiry/update owner and approved networking/CA. The secure profile remains
blocked until those real inputs are supplied. Do not replace its unresolved image
with a public mutable tag, disable TLS, introduce sudo/privilege or mount a host
Docker socket to make it open.

Use a separately approved builder with approved mirrors and CA. No repository
execution, dependency install or container build/opening happens on the secure
machine before [source/image admission](SECURE_TRANSITION.md). Source publication,
image admission, cloud-change approval and actual hosted acceptance retain their
distinct boundaries.
