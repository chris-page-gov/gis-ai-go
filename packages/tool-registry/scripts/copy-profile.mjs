import { copyFile, mkdir } from "node:fs/promises";

const source = new URL("../../../profiles/tool-registry.v1.json", import.meta.url);
const destinationDirectory = new URL("../dist/profile/", import.meta.url);
const destination = new URL("tool-registry.v1.json", destinationDirectory);

await mkdir(destinationDirectory, { recursive: true });
await copyFile(source, destination);
