# Third-party material

## HM Land Registry OKF metadata

GIS AI GO includes selected metadata inputs from
[`chris-page-gov/okf-LandRegistry` `v0.3.0`](https://github.com/chris-page-gov/okf-LandRegistry/releases/tag/v0.3.0),
created by Chris Page and licensed under CC BY 4.0 for original metadata, evaluation
and governance material. The exact upstream licence and provenance are preserved
under `okf/vendor/okf-landregistry/v0.3.0/`.

Attribution: “HM Land Registry public-estate OKF Bundle contributors, `v0.3.0`”,
linked to the release above and the
[CC BY 4.0 licence](https://creativecommons.org/licenses/by/4.0/). GIS AI GO
selects, normalises and adds explicit publication controls to the source metadata;
it does not imply upstream endorsement.

The derivative public bundle must attribute HM Land Registry and any named third
party according to each selected record. It contains metadata only. HMLR, GOV.UK,
Ordnance Survey, Royal Mail and other source content, names and trade marks retain
their own rights and conditions and are not relicensed by the GIS AI GO MIT licence.

## Public provider and source metadata

GIS AI GO also projects metadata-only descriptions of Office for National
Statistics and Land Information System capabilities from the dated, checksum-locked
research pack. The descriptions are original GIS AI GO research released under this
repository's MIT licence; the organisations, source services, datasets, names and
trade marks they describe retain their own rights.

ONS material is attributed to the Office for National Statistics. The Open
Government Licence applies only where the named ONS source or product says it does;
Ordnance Survey, Royal Mail and other third-party conditions remain product-specific.

LandIS material is attributed to Cranfield University and the Land Information
System. Its catalogue has mixed access and per-record rights. This repository does
not grant blanket reuse rights in LandIS records, services or data.

## Blocked gateway runtime composition

The DEPLOY-207 gateway candidate uses one fixed `linux/amd64` hybrid runtime. The
repository owner authorised use of the Red Hat Universal Base Image (UBI) terms on
24 August 2026. This is not a general permission to substitute another Red Hat
image, accept later terms or describe the resulting image as supported by Red Hat.

The realised root filesystem is composed from these immutable inputs:

- Red Hat UBI 10 micro runtime root
  `registry.access.redhat.com/ubi10-micro@sha256:422bd02268e317995a8fbb9c81c0835aa99798a234b5619c52350843d5ed5c4d`,
  including the exact `libgcc_s.so.1` dependency and its target;
- the official Node.js Docker image
  `node:24.19.0-bookworm-slim@sha256:3638d9a6fe4030bd716be989438248074489337ba3275657f93595428be4fc03`,
  used only as the build environment and donor for the upstream Node.js 24.19.0
  binary and its complete bundled licence notice; and
- Red Hat UBI 10 Node.js 24 minimal
  `registry.access.redhat.com/ubi10/nodejs-24-minimal@sha256:e0e44d118dfba1c90e8adbdc751d6db2a1c5f9b0856d31d577054f8ea5216e2d`,
  used only as the donor for the exact versioned `libstdc++` object and GCC runtime
  licence notices. The final stage creates the checked `libstdc++.so.6` SONAME link
  without network access.

The final image includes the unmodified March 2019
[Red Hat UBI EULA](https://www.redhat.com/licenses/EULA_Red_Hat_Universal_Base_Image_English_20190422.pdf)
at `/usr/share/licenses/gis-ai-go/RED_HAT_UBI_EULA.pdf`, SHA-256
`a07025b9f5b71a816febe6ac76f21c9f759c806fa0a66874af90a50c3293f1b6`.
The EULA continues to govern the UBI material. It permits redistribution subject to
its terms and the licences of the individual components. It does not grant Red Hat
maintenance, upgrades or support, and the final GIS AI GO labels expressly make no
Red Hat support or endorsement claim. The scratch composition supplies only GIS AI
GO product labels rather than inheriting either Red Hat image's product, vendor,
maintainer or display-name labels.

The copied Node binary has SHA-256
`bc17c508ffeed0ec622934f9b7fa72f8e78da65350e63c3eceb56fa688aa5e12`.
Its complete bundled licence file has SHA-256
`148eacf7863ef4329224a29398623077200a27194aa075569faf4a0a85566ca5`
and remains at `/usr/share/licenses/nodejs/LICENSE`. The corresponding official
upstream archive is
[`node-v24.19.0-linux-x64.tar.xz`](https://nodejs.org/download/release/v24.19.0/node-v24.19.0-linux-x64.tar.xz),
SHA-256
`14b342e71204f811bde6153be8e04b62aef63c236fef92b55f9c83154b409647`;
the tagged source is [Node.js v24.19.0](https://github.com/nodejs/node/tree/v24.19.0).

The realised GCC runtime objects are:

| Object | Provider | SHA-256 or link target |
| --- | --- | --- |
| `/usr/lib64/libgcc_s.so.1` | UBI micro runtime root | `libgcc_s-14-20251022.so.1` |
| `/usr/lib64/libgcc_s-14-20251022.so.1` | UBI micro runtime root | `a0070ef643f5ad08f3d3a32a439d8d02d388a38ba5732cbafe58f3a1d60f1e32` |
| `/usr/lib64/libstdc++.so.6` | Constructed link to the copied donor object | `libstdc++.so.6.0.33` |
| `/usr/lib64/libstdc++.so.6.0.33` | UBI Node.js 24 minimal donor | `6a76f822fa825d6a065358923c56f5569ac411b27987c035d6f61124a03016ee` |

The donor notices for the copied `libstdc++` object, including the GCC Runtime
Library Exception 3.1, remain under `/usr/share/licenses/libgcc/`. The remaining
direct Node dependencies and dynamic loader come from the exact UBI micro root.
Construction checks both link targets and all seven expected loader entries, rejects
any unresolved dependency and checks the Node, library, Node licence and UBI EULA
hashes before the image can be emitted.

Red Hat publishes corresponding source as source containers. The exact source
images for the redistributed UBI root and donor objects are:

- `registry.access.redhat.com/ubi10-micro:10.2-1786324819-source@sha256:2ed8c342b2121296998c202850b70aac10e9c4450aae60c51c828cec7a7d29f0`;
- `registry.access.redhat.com/ubi10/nodejs-24-minimal:10.2-1787229483-source@sha256:d64e6f3fd22629366c4e088fe8bd0694ce818f79d8e72bb7a3f74fc6fd672644`.

Use the Red Hat Ecosystem Catalog's documented source-container procedure with
`skopeo copy` rather than trying to run a source image. Any registry distribution
of the GIS AI GO image must retain this notice, all component licence directories,
the exact source references and the unmodified UBI EULA. Changing an input, copied
object, platform or support claim requires a new reviewed receipt and legal and
technical assurance; it is not covered by this fixed composition.
