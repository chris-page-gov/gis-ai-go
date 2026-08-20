import { types as utilTypes } from "node:util";

export type CanonicalJsonPrimitive = null | boolean | number | string;
export type CanonicalJsonValue =
  | CanonicalJsonPrimitive
  | readonly CanonicalJsonValue[]
  | { readonly [key: string]: CanonicalJsonValue };

export type CanonicalJsonErrorCode =
  | "accessor-property"
  | "cycle"
  | "invalid-array-property"
  | "invalid-number"
  | "invalid-object-property"
  | "invalid-string"
  | "non-plain-object"
  | "sparse-array"
  | "unsupported-type";

/** A structured description of a value that cannot be represented canonically. */
export class CanonicalJsonError extends TypeError {
  public readonly code: CanonicalJsonErrorCode;
  public readonly path: string;

  public constructor(code: CanonicalJsonErrorCode, path: string, message: string) {
    super(`Canonical JSON rejected ${path}: ${message}`);
    this.name = "CanonicalJsonError";
    this.code = code;
    this.path = path;
  }
}

function fail(code: CanonicalJsonErrorCode, path: string, message: string): never {
  throw new CanonicalJsonError(code, path, message);
}

function safePathForKey(parent: string, key: string): string {
  const rendered = JSON.stringify(key);
  return `${parent}[${rendered ?? '"<invalid>"'}]`;
}

function assertPairedSurrogates(value: string, path: string): void {
  for (let index = 0; index < value.length; index += 1) {
    const codeUnit = value.charCodeAt(index);
    if (codeUnit >= 0xd800 && codeUnit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) {
        fail("invalid-string", path, "contains an unpaired high surrogate");
      }
      index += 1;
      continue;
    }
    if (codeUnit >= 0xdc00 && codeUnit <= 0xdfff) {
      fail("invalid-string", path, "contains an unpaired low surrogate");
    }
  }
}

function ownKeys(value: object, path: string): readonly PropertyKey[] {
  try {
    return Reflect.ownKeys(value);
  } catch {
    return fail("non-plain-object", path, "own properties could not be inspected");
  }
}

function ownDescriptor(value: object, key: PropertyKey, path: string): PropertyDescriptor {
  try {
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    if (descriptor === undefined) {
      return fail("invalid-object-property", path, "an own property disappeared during inspection");
    }
    return descriptor;
  } catch {
    return fail("invalid-object-property", path, "an own property could not be inspected");
  }
}

function prototypeOf(value: object, path: string): object | null {
  try {
    return Object.getPrototypeOf(value) as object | null;
  } catch {
    return fail("non-plain-object", path, "the prototype could not be inspected");
  }
}

function serialiseArray(value: readonly unknown[], path: string, ancestors: WeakSet<object>): string {
  if (prototypeOf(value, path) !== Array.prototype) {
    return fail("non-plain-object", path, "array subclasses are not supported");
  }

  const keys = ownKeys(value, path);
  const indexDescriptors = new Map<number, PropertyDescriptor>();
  for (const key of keys) {
    if (typeof key !== "string") {
      return fail("invalid-array-property", path, "non-string properties are not supported");
    }
    if (key === "length") {
      continue;
    }
    if (!/^(?:0|[1-9][0-9]*)$/u.test(key)) {
      return fail("invalid-array-property", path, `unexpected property ${JSON.stringify(key)}`);
    }
    const index = Number(key);
    if (!Number.isSafeInteger(index) || index < 0 || index >= value.length || String(index) !== key) {
      return fail("invalid-array-property", path, `invalid array index ${JSON.stringify(key)}`);
    }
    const itemPath = `${path}[${index}]`;
    const descriptor = ownDescriptor(value, key, itemPath);
    if (!("value" in descriptor)) {
      return fail("accessor-property", itemPath, "accessor properties are not supported");
    }
    if (descriptor.enumerable !== true) {
      return fail("invalid-array-property", itemPath, "array items must be enumerable");
    }
    indexDescriptors.set(index, descriptor);
  }

  if (indexDescriptors.size !== value.length) {
    return fail("sparse-array", path, "every array index must be present");
  }

  const items = new Array<string>(value.length);
  for (const [index, descriptor] of indexDescriptors) {
    items[index] = serialise(descriptor.value, `${path}[${index}]`, ancestors);
  }
  return `[${items.join(",")}]`;
}

function serialiseObject(
  value: Record<string, unknown>,
  path: string,
  ancestors: WeakSet<object>,
): string {
  const prototype = prototypeOf(value, path);
  if (prototype !== Object.prototype && prototype !== null) {
    return fail("non-plain-object", path, "only plain objects are supported");
  }

  const descriptors = new Map<string, PropertyDescriptor>();
  for (const key of ownKeys(value, path)) {
    if (typeof key !== "string") {
      return fail("invalid-object-property", path, "non-string properties are not supported");
    }
    assertPairedSurrogates(key, `${path} property name`);
    const propertyPath = safePathForKey(path, key);
    const descriptor = ownDescriptor(value, key, propertyPath);
    if (!("value" in descriptor)) {
      return fail("accessor-property", propertyPath, "accessor properties are not supported");
    }
    if (descriptor.enumerable !== true) {
      return fail("invalid-object-property", propertyPath, "non-enumerable properties are not supported");
    }
    descriptors.set(key, descriptor);
  }

  // The default JavaScript comparison is defined over UTF-16 code units. Do not
  // replace this with localeCompare or code-point ordering.
  const keys = [...descriptors.keys()].sort();
  const entries = keys.map((key) => {
    const descriptor = descriptors.get(key);
    if (descriptor === undefined) {
      return fail("invalid-object-property", path, "a property disappeared during ordering");
    }
    const encodedKey = JSON.stringify(key);
    if (encodedKey === undefined) {
      return fail("invalid-string", safePathForKey(path, key), "the property name is invalid");
    }
    return `${encodedKey}:${serialise(descriptor.value, safePathForKey(path, key), ancestors)}`;
  });
  return `{${entries.join(",")}}`;
}

function serialise(value: unknown, path: string, ancestors: WeakSet<object>): string {
  if (value === null) {
    return "null";
  }
  switch (typeof value) {
    case "boolean":
      return value ? "true" : "false";
    case "number": {
      if (!Number.isFinite(value)) {
        return fail("invalid-number", path, "numbers must be finite");
      }
      const encoded = JSON.stringify(value);
      if (encoded === undefined) {
        return fail("invalid-number", path, "the number cannot be serialised");
      }
      return encoded;
    }
    case "string": {
      assertPairedSurrogates(value, path);
      const encoded = JSON.stringify(value);
      if (encoded === undefined) {
        return fail("invalid-string", path, "the string cannot be serialised");
      }
      return encoded;
    }
    case "object": {
      const objectValue = value as object;
      if (utilTypes.isProxy(objectValue)) {
        return fail("non-plain-object", path, "proxy objects are not supported");
      }
      if (ancestors.has(objectValue)) {
        return fail("cycle", path, "cyclic values are not supported");
      }
      ancestors.add(objectValue);
      try {
        return Array.isArray(value)
          ? serialiseArray(value, path, ancestors)
          : serialiseObject(value as Record<string, unknown>, path, ancestors);
      } finally {
        ancestors.delete(objectValue);
      }
    }
    case "bigint":
    case "function":
    case "symbol":
    case "undefined":
      return fail("unsupported-type", path, `${typeof value} is not part of the JSON data model`);
  }
  return fail("unsupported-type", path, "the value is not part of the JSON data model");
}

/**
 * Serialise a value using RFC 8785 JSON canonicalisation semantics. Values
 * outside the interoperable JSON data model are rejected rather than omitted or
 * coerced.
 */
export function canonicalJson(value: unknown): string {
  return serialise(value, "$", new WeakSet<object>());
}

/** Return a fresh UTF-8 byte sequence for the canonical JSON representation. */
export function canonicalJsonBytes(value: unknown): Uint8Array {
  return new TextEncoder().encode(canonicalJson(value));
}

function freezeJson(value: unknown): void {
  if (value === null || typeof value !== "object" || Object.isFrozen(value)) {
    return;
  }
  for (const child of Object.values(value)) {
    freezeJson(child);
  }
  Object.freeze(value);
}

/** Validate, detach and recursively freeze a value in the canonical JSON model. */
export function canonicalJsonClone<T>(value: T): T {
  const cloned = JSON.parse(canonicalJson(value)) as T;
  freezeJson(cloned);
  return cloned;
}
