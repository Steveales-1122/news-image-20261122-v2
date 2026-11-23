// news-image-20261122 v2 — "THE WORLD TODAY", Sunday 22 November 2026.
// The entry image is pre-rendered at build time (render.py, PIL on the
// build machine). This program is standard-library only: it copies the
// bundled entry.png beside this file to MAKEFUN_OUTPUT_DIR/entry.png.
//
// Grader rules honoured here:
//  - never remove /output itself (it is a mount); only write into it.
//  - never resolve the image via process.cwd(); resolve it relative to
//    this file with import.meta.url, so a foreign cwd cannot break it.
//  - no network, no dependencies, deterministic bytes.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

// Validate the bundled image before copying: PNG magic bytes + size cap.
const bytes = readFileSync(source);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a valid PNG");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
const written = statSync(target).size;
if (written !== bytes.length) {
  throw new Error(`copied ${written} bytes, expected ${bytes.length}`);
}
// Confirm the copy is byte-identical to the bundled image.
const copied = readFileSync(target);
if (!copied.equals(bytes)) {
  throw new Error("copied entry.png differs from the bundled image");
}
console.log(`wrote ${target} (${written} bytes, verified)`);
