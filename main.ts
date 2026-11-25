// news-image-20261125 entry (Node 22, standard library only).
// Draws "THE WORLD IN ONE DAY" (Wednesday 25 November 2026) with generate.py
// (Python + PIL), and falls back to the bundled entry.png when Python or PIL
// is unavailable, so the program still writes a whole, valid PNG either way.
//
// Outside the grader's container, OUTPUT_DIR (or MAKEFUN_OUTPUT_DIR) stands
// in for /output:
//   mkdir -p out && OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.OUTPUT_DIR ?? process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outPath = join(outDir, 'entry.png');
const script = join(repoDir, 'generate.py');
const bundled = join(repoDir, 'entry.png');

mkdirSync(outDir, { recursive: true });

let drawn = false;
if (existsSync(script)) {
  for (const cmd of ['python3', 'python']) {
    const run = spawnSync(cmd, [script, outDir], { cwd: repoDir, encoding: 'utf8' });
    if (run.status === 0 && existsSync(outPath)) {
      drawn = true;
      break;
    }
  }
}
if (!drawn) {
  copyFileSync(bundled, outPath);
}

const bytes = readFileSync(outPath);
if (bytes.length < 8 || bytes.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png is not a PNG');
}
if (bytes.subarray(12, 16).toString('ascii') !== 'IHDR') {
  throw new Error('entry.png has no IHDR chunk');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}
if (bytes.subarray(-12).toString('hex') !== '0000000049454e44ae426082') {
  throw new Error('entry.png has no intact IEND trailer');
}
const sha256 = createHash('sha256').update(bytes).digest('hex');
console.log(`entry.png ${width}x${height} ${bytes.length} bytes sha256 ${sha256} (${drawn ? 'drawn' : 'bundled fallback'})`);
