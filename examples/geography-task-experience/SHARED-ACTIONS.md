# Shared local overlay actions

The task navigator, reference tabs and pin control use one validated action
implementation when `shared_actions.js` is loaded. A future page adapter can
call the same implementation without simulating a click. This increment supplies
the local implementation and synthetic tests; it registers no page or MCP tools,
changes no hosted Site and adds no provider connection.

The owner is the GIS AI GO product maintainer. The
[action schema](shared-actions.schema.json) defines a closed serialisable
`{action, input}` envelope and results at `#/$defs/result`. The in-process method
receives `action` and `input` separately. Its optional `AbortSignal` is not part
of that serialised envelope.

| Action | Input | Effect |
| --- | --- | --- |
| `read-state` | Empty object | Read four routing and presentation fields. |
| `open-task` | Exact `taskId` and boolean `focus` | Select one of the seven existing tasks. |
| `open-reference` | Exact `referenceId` and boolean `focus` | Open the inspector and select one of its four tabs. |
| `set-pinned` | Boolean `pinned` | Set the pin explicitly; repeating the value does not toggle it. |

State contains only `taskId`, `referenceId`, `pinned` and `referenceOpen`. Every
legal result fits within 512 UTF-8 bytes. It contains no selected feature,
glossary text, file content, URL, customer record or host exception. Read state
is not an authorisation token or a durable evidence receipt.

## Host integration and policy

Load `shared_actions.js` before `experience.js`, then initialise the overlay
after constructing its DOM as described in the [host guide](README.md).
`initialiseExperience()` creates the adapter with the existing task, reference
and pin functions. Callers in the same trusted page can use
`experienceSharedActions.execute('open-task', {taskId: 'areas', focus: true})`.
The same task function retains its focus, URL fragment, history and pinned
reference behaviour. An explicit reference action opens a hidden inspector.

The adapter is trusted, synchronous application code. Returning deferred work is
outside its contract. Validated inputs are copied from own data descriptors into
fresh frozen snapshots before invoking callbacks. Unknown IDs, including
prototype-like names, extra properties, accessors and coercible booleans are
refused before a setter. State is checked before and after each action, followed
by an action-specific postcondition. Host error metadata is inspected once as an
own data descriptor; getters and raw exception text never enter the result.

Cancellation is checked at entry and immediately before a setter.
Cancellation or failure after setter entry reports
`mutationMayHaveOccurred: true`. This does not promise rollback or make an
automatic retry safe. The operation is short and synchronous; it does not add
a worker, background job or asynchronous cancellation mechanism.

When the optional module is absent, manual controls keep their existing
behaviour. When it is present, a refusal never falls back to an unvalidated
action. History, skip links and other learning controls keep their existing
internal functions. This is a boundary for the four named actions, not a claim
that every internal UI helper accepts untrusted input safely.

## Threat and acceptance boundary

The threat model covers unchecked task IDs, changing Proxy/accessor values,
callbacks mutating input after validation, host-state disclosure, exception
disclosure and late cancellation being mistaken for rollback. Closed snapshots,
finite result codes, exact state projection and postconditions address those
cases. The module adds no arbitrary selector, URL, HTML, script, model, file,
provider, credential or persistence parameter.

Any future transport must bound bytes before parsing, validate its own envelope,
apply host/session policy and pass the invocation's cancellation signal. Page
tool registration, lifecycle and disclosure remain separate work under the
[page-tools boundary](../../docs/decisions/ADR-0013-webmcp-page-tools-boundary.md).
A remote server cannot claim to have changed a person's visible browser without
an admitted session and state contract. No proposed adapter is deployed here.

The canonical `test:experience` command runs 41 core/adverse tests, 29 overlay
integration checks and 22 repeated checks with the module absent. The unchanged
53 code-list checks also remain in that suite. The core tests exercise the
browser-global loader through Node's VM in the repository's `type: module`
package; they do not depend on CommonJS loading of a `.js` asset. All fixtures
are public and synthetic. Exact schema IDs, closed fields, all legal state
combinations, cancellation and hostile input/error behaviour are checked.

These checks establish source behaviour in a synthetic DOM. Rendered layout,
assistive technology, human learning, a compatible AI host and the exact deployed
Site each require their own acceptance evidence. Full canonical CI remains
mandatory; local results do not replace it.
