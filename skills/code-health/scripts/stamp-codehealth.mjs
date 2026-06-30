#!/usr/bin/env node
//
// Stamp current CodeHealth readings into hand-authored wiki/markdown pages so they
// don't go stale. Reads <historyDir>/codehealth-stamp.json (written by
// codehealth-report.mjs — run it first) and fills every
// `<!--ch:NAME-->…<!--/ch:NAME-->` marker. Block markers (chart, pie, hotspot_table)
// sit OUTSIDE code fences — HTML comments can't live inside one — so the whole
// block regenerates while the markers stay invisible. Idempotent.
//
//   node stamp-codehealth.mjs <file.md>...
//
import fs from 'node:fs';
import { hist } from './config.mjs';

const STAMP = hist('codehealth-stamp.json');
const targets = process.argv.slice(2);
if (!targets.length) { console.error('usage: stamp-codehealth.mjs <file.md>...'); process.exit(1); }
if (!fs.existsSync(STAMP)) { console.error(`${STAMP} missing — run the codehealth report first`); process.exit(1); }

const s = JSON.parse(fs.readFileSync(STAMP, 'utf8'));
const VALUES = {};
for (const [k, v] of Object.entries(s)) {
  const str = String(v);
  VALUES[k] = str.includes('\n') ? `\n${str}\n` : str;
}

let stamped = 0;
for (const f of targets) {
  const src = fs.readFileSync(f, 'utf8');
  let out = src;
  for (const [name, val] of Object.entries(VALUES)) {
    out = out.replace(new RegExp(`(<!--ch:${name}-->)[\\s\\S]*?(<!--/ch:${name}-->)`, 'g'), (_m, p1, p2) => `${p1}${val}${p2}`);
  }
  if (out !== src) { fs.writeFileSync(f, out); stamped++; console.log(`  stamped ${f}`); }
  else console.log(`  already current: ${f}`);
}
console.log(`\nCodeHealth ${s.badge} · ${s.files} files · ${s.loc} LOC — ${stamped} file(s) updated`);
