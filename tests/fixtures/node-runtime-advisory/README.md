# Reviewed public advisory prose

`CVE-2026-105482.json` is the unchanged public CVEProject record at
[commit 1d00567453bd67f89f5c2f37c29673e6d194080a](https://github.com/CVEProject/cvelistV5/blob/1d00567453bd67f89f5c2f37c29673e6d194080a/cves/2026/105xxx/CVE-2026-105482.json).
The whole retained file has SHA-256
`4741deb16926e3245564d15c2a47929fb1a31fafe85dbab9d81f9081b5262d17`.

The English CNA description contains 670 UTF-8 bytes, with SHA-256
`4860b19ad9d60392ad2fb11103fc786e634469d26db9ecc7692591ac06967f01`.
Its public DNS example contains a literal backslash followed by zero. There is no
actual NUL byte in the description. Decoding the documentary escape as a control
character caused the generic privacy guard to withhold an otherwise public scan
report before evaluating its findings.

Only these exact description bytes, under the exact JSON member `description`
with the same object's exact `id` of `CVE-2026-105482`, retain their original literal
meaning during privacy inspection. All size, depth and node limits, enclosing
credential checks and sibling inspection remain active. Changed prose, other
contexts and actual control bytes receive the original checks. Raw scanner
reports are retained unchanged and remain bound to offline replay.

This compatibility rule does not suppress the CVE, change its severity, admit an
affected runtime, or alter the High/Critical vulnerability or calibration gates.
The actual runtime must still use the separately verified patched Node release.
