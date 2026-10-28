# Interpreting schema diagnostics before reporting a discrepancy

A schema describes the allowed shape and values of data. A **metaschema** is a
schema used to check that the schema itself is correctly formed. Keep these two
checks separate: a schema diagnostic does not, by itself, show that delivered
features are wrong or that a current service is failing.

Use the declared schema language and version. The examples below use fictional
fields and [JSON Schema Draft 7 validation](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01).
They are teaching examples, not copies of supplier responses or proposed fixes.

## Constraints apply together

An **enumeration** is the explicitly allowed set of values. In this example,
`type` permits strings or null, but `enum` permits only one string:

```json
{"type": ["string", "null"], "enum": ["Example"]}
```

`"Example"` passes and `null` fails. The constraints intersect: permission from
one keyword does not override another keyword. A nullable type combined with an
enumeration that excludes null is therefore not inherently a contradiction.
Check whether the documented intended value set differs before proposing a
change. Do not add null to every enumeration or silently relax a retained schema.
See Draft 7 sections 6.1.1 and 6.1.2.

## A valid schema can exclude every object

In this fictional example the required name differs in case from the declared
property, and additional properties are forbidden:

```json
{
  "properties": {"exampleName": {"type": "string"}},
  "required": ["ExampleName"],
  "additionalProperties": false
}
```

Every object fails: omitting `ExampleName` fails `required`; including it fails
`additionalProperties`. Property names are exact strings. This can be a
metaschema-valid schema even though it admits no object. Because no root `type`
is declared, a non-object such as `null` can still pass. Report the precise
result as “no object satisfies these constraints”, not “no JSON value can pass”.
See Draft 7 sections 6.5.3 and 6.5.6 and its applicability rules.

## Check the schema itself before feature validation

Examples of Draft 7 metaschema failures include a non-standard type name, a
non-integer `maxLength`, a null `maxItems`, or a null `description`. Keep the
native JSON type: null is not a string, an absent property or zero. An invalid
annotation such as `description` concerns schema conformance; it does not
establish an invalid feature value or service outage. Keep all reported
locations, including failures that occur in the same document.

A reference such as `$ref` can depend on an external schema. Record whether that
reference was resolved, its exact version and bytes, and the applicable draft's
reference semantics. A local check over unresolved references must state its
limits. Do not extend a bounded request selection merely because a response
contains another URL.

## Retain dated, reproducible evidence

For each finding, retain the original schema bytes and hash, exact keyword
location, declared draft, collection and version, retrieval time, complete
request shape with credentials removed, validator version and result. Include
small positive and negative controls and distinguish the complete schema from
any reduced explanatory example. A reduced example demonstrates the selected
interaction; it does not replace a complete source check.

Separate a confirmed finding in retained bytes from a current-service
reproduction, supplier intent and a proposed correction. Publication, collection,
reference, feature-validity and retrieval dates have different roles. A second
source can legitimately use another scheme, edition or representation.

Any derived profile must retain the original strict result, identify every
changed constraint and remain separately reviewed and version-bound. A derived
pass does not convert a strict failure into a pass. The
[identifier-bridge method](OS_IDENTIFIER_GEOGRAPHY_BRIDGES.md) and
[documentary findings](../research/2026-10-22/NGD_RAMI_DOCUMENTARY_METHOD.md)
apply these distinctions to selected geospatial evidence. No provider request,
source repair, public payload or supplier submission is authorised by this note.
