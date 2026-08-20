const NUMBER = /-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/uy;
const HEX = /^[0-9A-Fa-f]{4}$/u;

const MAX_DEPTH = 32;
const MAX_VALUES = 20_000;

export class StrictJsonParseError extends SyntaxError {
  public constructor() {
    super("Provider JSON did not meet the strict parsing contract");
    this.name = "StrictJsonParseError";
  }
}

function fail(): never {
  throw new StrictJsonParseError();
}

function assertPairedSurrogates(value: string): void {
  for (let index = 0; index < value.length; index += 1) {
    const codeUnit = value.charCodeAt(index);
    if (codeUnit >= 0xd800 && codeUnit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) fail();
      index += 1;
    } else if (codeUnit >= 0xdc00 && codeUnit <= 0xdfff) {
      fail();
    }
  }
}

/**
 * Parse bounded JSON while rejecting duplicate decoded object keys. `JSON.parse`
 * alone silently accepts the last duplicate, which is unsafe at a provider trust
 * boundary.
 */
export function parseStrictJson(text: string): unknown {
  let index = 0;
  let values = 0;

  const whitespace = (): void => {
    while (index < text.length && /[\u0009\u000a\u000d\u0020]/u.test(text[index]!)) {
      index += 1;
    }
  };

  const stringValue = (): string => {
    if (text[index] !== '"') fail();
    const start = index;
    index += 1;
    while (index < text.length) {
      const code = text.charCodeAt(index);
      if (code === 0x22) {
        index += 1;
        try {
          const parsed = JSON.parse(text.slice(start, index)) as string;
          assertPairedSurrogates(parsed);
          return parsed;
        } catch {
          return fail();
        }
      }
      if (code < 0x20) fail();
      if (code === 0x5c) {
        index += 1;
        const escape = text[index];
        if (escape === undefined || !'"\\/bfnrtu'.includes(escape)) fail();
        if (escape === "u") {
          const digits = text.slice(index + 1, index + 5);
          if (!HEX.test(digits)) fail();
          index += 4;
        }
      }
      index += 1;
    }
    return fail();
  };

  const value = (depth: number): unknown => {
    if (depth > MAX_DEPTH || ++values > MAX_VALUES) fail();
    whitespace();
    const first = text[index];
    if (first === '"') return stringValue();
    if (first === "{") {
      index += 1;
      whitespace();
      const result: Record<string, unknown> = Object.create(null) as Record<string, unknown>;
      const keys = new Set<string>();
      if (text[index] === "}") {
        index += 1;
        return result;
      }
      while (true) {
        whitespace();
        const key = stringValue();
        if (keys.has(key)) fail();
        keys.add(key);
        whitespace();
        if (text[index] !== ":") fail();
        index += 1;
        result[key] = value(depth + 1);
        whitespace();
        if (text[index] === "}") {
          index += 1;
          return result;
        }
        if (text[index] !== ",") fail();
        index += 1;
      }
    }
    if (first === "[") {
      index += 1;
      whitespace();
      const result: unknown[] = [];
      if (text[index] === "]") {
        index += 1;
        return result;
      }
      while (true) {
        result.push(value(depth + 1));
        whitespace();
        if (text[index] === "]") {
          index += 1;
          return result;
        }
        if (text[index] !== ",") fail();
        index += 1;
      }
    }
    for (const [literal, parsed] of [
      ["true", true],
      ["false", false],
      ["null", null],
    ] as const) {
      if (text.startsWith(literal, index)) {
        index += literal.length;
        return parsed;
      }
    }
    NUMBER.lastIndex = index;
    const match = NUMBER.exec(text);
    if (match === null) fail();
    index = NUMBER.lastIndex;
    const parsed = Number(match[0]);
    if (!Number.isFinite(parsed) || (Number.isInteger(parsed) && !Number.isSafeInteger(parsed))) {
      fail();
    }
    return Object.is(parsed, -0) ? 0 : parsed;
  };

  const parsed = value(0);
  whitespace();
  if (index !== text.length) fail();
  return parsed;
}
