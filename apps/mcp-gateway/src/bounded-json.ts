/** Strict bounded JSON shared by direct HTTP and MCP; no application imports. */
const JSON_NUMBER = /^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/u;
const MAX_JSON_NESTING = 16;
const MAX_CONFIGURED_JSON_BODY_BYTES = 1_048_576;

export type BoundedJsonFailure = "duplicate" | "malformed" | "too_large";

export class BoundedJsonError extends Error {
  public constructor(public readonly failure: BoundedJsonFailure) {
    super(failure);
    this.name = "BoundedJsonError";
  }
}

function hasValidUnicodeScalars(value: string): boolean {
  for (let index = 0; index < value.length; index += 1) {
    const unit = value.charCodeAt(index);
    if (unit >= 0xd800 && unit <= 0xdbff) {
      const next = value.charCodeAt(index + 1);
      if (!(next >= 0xdc00 && next <= 0xdfff)) return false;
      index += 1;
    } else if (unit >= 0xdc00 && unit <= 0xdfff) {
      return false;
    }
  }
  return true;
}

class StrictJsonScanner {
  private index = 0;

  public constructor(private readonly text: string) {}

  public scan(): void {
    this.skipWhitespace();
    this.scanValue(0);
    this.skipWhitespace();
    if (this.index !== this.text.length) this.malformed();
  }

  private malformed(): never {
    throw new BoundedJsonError("malformed");
  }

  private skipWhitespace(): void {
    while (
      this.text[this.index] === " " ||
      this.text[this.index] === "\t" ||
      this.text[this.index] === "\n" ||
      this.text[this.index] === "\r"
    ) {
      this.index += 1;
    }
  }

  private scanValue(depth: number): void {
    if (depth > MAX_JSON_NESTING) this.malformed();
    const token = this.text[this.index];
    if (token === "{") {
      this.scanObject(depth);
      return;
    }
    if (token === "[") {
      this.scanArray(depth);
      return;
    }
    if (token === '"') {
      this.scanString();
      return;
    }
    if (token === "t") {
      this.scanLiteral("true");
      return;
    }
    if (token === "f") {
      this.scanLiteral("false");
      return;
    }
    if (token === "n") {
      this.scanLiteral("null");
      return;
    }
    this.scanNumber();
  }

  private scanObject(depth: number): void {
    this.index += 1;
    this.skipWhitespace();
    const keys = new Set<string>();
    if (this.text[this.index] === "}") {
      this.index += 1;
      return;
    }
    while (this.index < this.text.length) {
      if (this.text[this.index] !== '"') this.malformed();
      const key = this.scanString();
      if (keys.has(key)) throw new BoundedJsonError("duplicate");
      keys.add(key);
      this.skipWhitespace();
      if (this.text[this.index] !== ":") this.malformed();
      this.index += 1;
      this.skipWhitespace();
      this.scanValue(depth + 1);
      this.skipWhitespace();
      const separator = this.text[this.index];
      if (separator === "}") {
        this.index += 1;
        return;
      }
      if (separator !== ",") this.malformed();
      this.index += 1;
      this.skipWhitespace();
    }
    this.malformed();
  }

  private scanArray(depth: number): void {
    this.index += 1;
    this.skipWhitespace();
    if (this.text[this.index] === "]") {
      this.index += 1;
      return;
    }
    while (this.index < this.text.length) {
      this.scanValue(depth + 1);
      this.skipWhitespace();
      const separator = this.text[this.index];
      if (separator === "]") {
        this.index += 1;
        return;
      }
      if (separator !== ",") this.malformed();
      this.index += 1;
      this.skipWhitespace();
    }
    this.malformed();
  }

  private scanString(): string {
    const start = this.index;
    this.index += 1;
    while (this.index < this.text.length) {
      const unit = this.text.charCodeAt(this.index);
      if (unit < 0x20) this.malformed();
      if (this.text[this.index] === '"') {
        this.index += 1;
        let decoded: unknown;
        try {
          decoded = JSON.parse(this.text.slice(start, this.index));
        } catch {
          this.malformed();
        }
        if (typeof decoded !== "string" || !hasValidUnicodeScalars(decoded)) {
          this.malformed();
        }
        return decoded;
      }
      if (this.text[this.index] === "\\") {
        this.index += 1;
        const escaped = this.text[this.index];
        if (escaped === "u") {
          if (
            !/^[0-9a-fA-F]{4}$/u.test(
              this.text.slice(this.index + 1, this.index + 5),
            )
          ) {
            this.malformed();
          }
          this.index += 5;
          continue;
        }
        if (escaped === undefined || !'"\\/bfnrt'.includes(escaped)) this.malformed();
      }
      this.index += 1;
    }
    this.malformed();
  }

  private scanLiteral(literal: string): void {
    if (this.text.slice(this.index, this.index + literal.length) !== literal) {
      this.malformed();
    }
    this.index += literal.length;
  }

  private scanNumber(): void {
    const match = JSON_NUMBER.exec(this.text.slice(this.index));
    if (match?.[0] === undefined || !Number.isFinite(Number(match[0]))) this.malformed();
    this.index += match[0].length;
  }
}

function assertMaximumBodyBytes(maximumBytes: number): void {
  if (
    !Number.isSafeInteger(maximumBytes) ||
    maximumBytes < 1 ||
    maximumBytes > MAX_CONFIGURED_JSON_BODY_BYTES
  ) {
    throw new TypeError("maximum JSON body bytes must be an integer from 1 to 1048576");
  }
}

/** Parse one strict UTF-8 JSON value with duplicate-key and nesting protection. */
export function parseBoundedJsonBytes(
  bytes: Uint8Array,
  maximumBytes: number,
): unknown {
  assertMaximumBodyBytes(maximumBytes);
  if (!(bytes instanceof Uint8Array)) throw new TypeError("JSON body must be bytes");
  if (bytes.byteLength > maximumBytes) throw new BoundedJsonError("too_large");
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
  } catch {
    throw new BoundedJsonError("malformed");
  }
  new StrictJsonScanner(text).scan();
  try {
    return JSON.parse(text) as unknown;
  } catch {
    throw new BoundedJsonError("malformed");
  }
}
