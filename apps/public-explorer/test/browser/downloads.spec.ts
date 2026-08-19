import { expect, test } from "../fixtures/assurance";

test("offers the governed projections and checksum ledger as local downloads", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Download catalogue/i })).toBeVisible();

  const json = page.getByRole("link", { name: /^(?:Download )?JSON$/i });
  const jsonLd = page.getByRole("link", { name: /^(?:Download )?JSON-LD$/i });
  const checksums = page.getByRole("link", {
    name: /^(?:Download )?(?:checksums|CHECKSUMS\.sha256)$/i,
  });
  await expect(json).toHaveAttribute("href", /catalogue\/okf-bundle\.json$/);
  await expect(jsonLd).toHaveAttribute("href", /catalogue\/okf-bundle\.jsonld$/);
  await expect(checksums).toHaveAttribute("href", /catalogue\/CHECKSUMS\.sha256$/);

  const checksumReport = await page.evaluate(async () => {
    const ledgerResponse = await fetch("./catalogue/CHECKSUMS.sha256", { cache: "no-store" });
    if (!ledgerResponse.ok) {
      return { entries: 0, failures: [`ledger returned ${ledgerResponse.status}`] };
    }
    const lines = (await ledgerResponse.text()).trimEnd().split("\n");
    const failures: string[] = [];
    let entries = 0;
    for (const line of lines) {
      const match = /^([0-9a-f]{64}) {2}(.+)$/u.exec(line);
      if (match?.[1] === undefined || match[2] === undefined) {
        failures.push(`invalid checksum row: ${line}`);
        continue;
      }
      entries += 1;
      const response = await fetch(`./catalogue/${match[2]}`, { cache: "no-store" });
      if (!response.ok) {
        failures.push(`${match[2]} returned ${response.status}`);
        continue;
      }
      const bytes = await response.arrayBuffer();
      const digest = [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))]
        .map((value) => value.toString(16).padStart(2, "0"))
        .join("");
      if (digest !== match[1]) failures.push(`${match[2]} checksum mismatch`);
    }
    return { entries, failures };
  });

  expect(checksumReport.entries).toBeGreaterThan(0);
  expect(checksumReport.failures).toEqual([]);
});

test("downloaded JSON and JSON-LD expose the same record identifiers", async ({ page }) => {
  await page.goto("/");

  const identifiers = await page.evaluate(async () => {
    const [jsonResponse, jsonLdResponse] = await Promise.all([
      fetch("./catalogue/okf-bundle.json"),
      fetch("./catalogue/okf-bundle.jsonld"),
    ]);
    if (!jsonResponse.ok || !jsonLdResponse.ok) {
      throw new Error(`projection download failed: ${jsonResponse.status}/${jsonLdResponse.status}`);
    }
    const json = (await jsonResponse.json()) as { records: Array<{ id: string }> };
    const jsonLd = (await jsonLdResponse.json()) as {
      "@graph": Array<{ identifier: string }>;
    };
    return {
      json: json.records.map((record) => record.id).sort(),
      jsonLd: jsonLd["@graph"].map((record) => record.identifier).sort(),
    };
  });

  expect(identifiers.json.length).toBeGreaterThan(0);
  expect(identifiers.jsonLd).toEqual(identifiers.json);
});
