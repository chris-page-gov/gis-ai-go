# Sites pilot: OS and ONS rights assessment

Assessed on 1 October 2026. This is a bounded technical admission assessment,
not a substitute for the organisation's interpretation of its agreements.
Entitlement and account details are held privately.

## Initial decision

Enable only the reviewed open-data routes: OS Open Names place discovery, OS open
product metadata, ONS maintained CPIH and the fixed ONS MSOA 2021 names/codes table.
Do not enable protected address or feature payloads under PSGA at this checkpoint.
The owner has identified an organisational entitlement and authorised the existing
credential, but the specific third-party hosting and AI-use conditions have not
yet been evidenced. This is a conditional decision, not a finding that all cloud
or AI use is prohibited.

| Route | Source and conditions | Pilot decision |
| --- | --- | --- |
| OS Names API | [Product](https://www.ordnancesurvey.co.uk/products/os-names-api) and [find contract](https://docs.os.uk/os-apis/accessing-os-apis/os-names-api/technical-specification/find). OpenData place, road and postcode discovery; requires a configured credential. | At most five candidates. Retain native identifiers, GB coverage, representative-point meaning and OS/Royal Mail/National Statistics acknowledgements. |
| OS Downloads product metadata | [Contract](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification). OpenData metadata is keyless. | Fixed three-product allowlist; no archive download or claim to have queried its contents. |
| ONS CPIH | [Maintained API migration](https://developer.ons.gov.uk/retirement/v0api/). L522/MM23 identity, release and index unit are checked. | Open Government Licence attribution; preserve source release and observation month. Arithmetic does not turn index levels into a separately published inflation measure. |
| ONS MSOA names/codes | [ONS geography licences](https://www.ons.gov.uk/methodology/geography/licences). Fixed December 2021 England-and-Wales names/codes table. | Retain GSS codes, vintage, attribution and explicit partial-page status. No boundary payload, point containment or property inference. |
| OS Places | [Product](https://www.ordnancesurvey.co.uk/products/os-places-api). Address data has separate addressing and end-user rights. | Disabled pending product/purpose/recipient admission. An open named place is not an equivalent address lookup. |
| OS NGD Features | [Feature contract](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/features). Collection-specific protected feature access. | Disabled; no arbitrary collection, bounding-box or CQL proxy. |

## What would permit a PSGA extension

Check the current [PSGA Member Licence](https://www.ordnancesurvey.co.uk/documents/licensing/psga-member-licence.pdf)
and applicable product terms against the actual member, project, purpose and
recipients. The currently linked member licence is version 3.0, May 2024.
The assessment must establish:

1. The member's authority for this project and the applicable core-business use.
2. Whether the Sites host, any service provider and the consuming AI client are
   permitted recipients, with the required [contractor arrangements](https://www.ordnancesurvey.co.uk/licensing/public-sector-contractor-licence).
3. Product-specific storage, caching, onward sharing, model processing, retention,
   deletion and output conditions, including any addressing rights.
4. The organisation's approval for the actual account, access controls, processing
   location and contractual arrangements. [Sites currently gives no residency
   guarantee](https://learn.chatgpt.com/docs/sites).
5. Appropriate [copyright acknowledgements](https://www.ordnancesurvey.co.uk/customers/public-sector/public-sector-licensing/copyright-acknowledgments)
   and licence identifiers for permitted outputs.

Owner-only access and a functioning API key establish neither this recipient
chain nor all contractual conditions. No inference is made from the absence of
an explicit AI or cloud clause in a general licence. The current implementation
does not request PSGA payloads, accept provider terms or change account settings.

## Operational conditions

Keep credentials server-side and secret. OS authentication uses the documented
[`key` header](https://docs.os.uk/os-apis/core-concepts/authentication), never a
URL parameter, result, public artefact or browser variable. Do not forward it to
ONS or OS keyless metadata endpoints. All source payloads remain untrusted data.

The application initially admits at most 120 attempts per provider, with at most
20 attempts in its fixed one-minute window, counted before each fetch. There is
no refund after cancellation or failure. These are deliberately small pilot
bounds, not provider tariffs or a Sites billing guarantee. The published OS
[rate policy](https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy) and
ONS [request guidance](https://developer.ons.gov.uk/bots/) are separate source
limits. No chargeable provider operation or automatic top-up is enabled.

Reassess rights before adding a dataset or client. A future protected result must
never enter the public repository, public test fixtures or public evaluation
reports. The open-data fallback remains a useful independently testable profile.
