#!/usr/bin/env node
//
// dev-onboarding · doctor — READ-ONLY cold-start health check. Detects missing
// tools, wrong versions, and absent/malformed env secrets, and prints the EXACT
// fix for every red line. Never mutates. Exit 0 if all required checks pass, 1
// otherwise (CI-friendly). Mirrors the project's two onboarding paths via
// `--profile team|contributor`.
//
//   node doctor.mjs [--profile team|contributor] [--services]
//
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import {
  PROJECT, REQUIRED_TOOLS, ENV_EXAMPLE, ENV_FILE, RUN_COMMAND, HEALTH_ENDPOINTS,
  CONFIG_PRESENT, parseProfile, secretsForProfile, c, ICON,
} from './config.mjs';

const argv = process.argv.slice(2);
const profile = parseProfile(argv, 'team');
const checkServices = argv.includes('--services');

const rows = []; // { state: 'ok'|'bad'|'warn', label, detail, fix }
const add = (state, label, detail = '', fix = '') => rows.push({ state, label, detail, fix });

// ── version helpers ─────────────────────────────────────────────────────────
const sh = (cmd) => { try { return execSync(cmd, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim(); } catch { return null; } };
const semver = (s) => { const m = String(s).match(/(\d+)\.(\d+)\.(\d+)/) || String(s).match(/(\d+)\.(\d+)/) || String(s).match(/(\d+)/); return m ? [Number(m[1] || 0), Number(m[2] || 0), Number(m[3] || 0)] : null; };
function satisfies(version, range) {
  const v = semver(version); if (!v) return false;
  range = String(range).trim();
  let m;
  if ((m = range.match(/^(\d+)\.x$/))) return v[0] === Number(m[1]);            // 20.x
  if ((m = range.match(/^>=\s*(\d+)\.(\d+)\.(\d+)/))) {                          // >=10.8.0
    const r = [Number(m[1]), Number(m[2]), Number(m[3])];
    for (let i = 0; i < 3; i++) { if (v[i] > r[i]) return true; if (v[i] < r[i]) return false; }
    return true;
  }
  if ((m = range.match(/^(\d+)/))) return v[0] === Number(m[1]);                // "20"
  return true;
}
function rangeFor(tool) {
  if (tool.versionFrom && fs.existsSync(tool.versionFrom)) return fs.readFileSync(tool.versionFrom, 'utf8').trim();
  return tool.range || null;
}

// ── 1. environment (informational) ──────────────────────────────────────────
const plat = `${os.type()} ${os.release().split('-')[0]} (${os.arch()})`;
const isWSL = /microsoft/i.test(os.release());
add('ok', 'Platform', plat + (isWSL ? ' · WSL' : ''));

// ── 2. tools ────────────────────────────────────────────────────────────────
for (const tool of REQUIRED_TOOLS) {
  const ver = sh(`${tool.name} --version`);
  const range = rangeFor(tool);
  if (!ver) {
    if (tool.optional) add('warn', tool.name, 'not installed', tool.installHint || (tool.reason ? `optional — ${tool.reason}` : 'optional'));
    else add('bad', tool.name, 'not found', tool.installHint || `install ${tool.name}` + (range ? ` ${range}` : ''));
    continue;
  }
  const v = (semver(ver) || []).join('.');
  if (range && !satisfies(ver, range)) {
    add('bad', tool.name, `${v} (need ${range})`, tool.installHint || `install ${tool.name} ${range} (e.g. \`nvm install\` reads .nvmrc)`);
  } else {
    add('ok', tool.name, v + (range ? ` (${range})` : ''));
  }
}

// ── 3. env file + secret shape ──────────────────────────────────────────────
const envExists = fs.existsSync(ENV_FILE);
if (!envExists) {
  add('bad', ENV_FILE, 'missing', `cp ${ENV_EXAMPLE} ${ENV_FILE}  # then fill in the secrets below`);
} else {
  add('ok', ENV_FILE, 'present');
}
const envText = envExists ? fs.readFileSync(ENV_FILE, 'utf8') : '';
const envVal = (k) => {
  const m = envText.match(new RegExp(`^\\s*${k}\\s*=\\s*["']?([^"'\\n#]*)`, 'm'));
  return m ? m[1].trim() : '';
};
for (const [name, spec] of secretsForProfile(profile)) {
  const val = envVal(name);
  const placeholderish = /^(your[-_]|xxx|changeme|<|\.\.\.)|here$/i.test(val);
  if (!val || placeholderish) {
    const mock = spec.mockToggle ? ` — or set ${spec.mockToggle}=true to skip` : '';
    add('bad', name, val ? 'placeholder' : 'not set', (spec.getFrom || spec.help || 'set this secret') + mock);
  } else if (spec.shape && !new RegExp(spec.shape).test(val)) {
    add('warn', name, "set, but doesn't match expected shape", spec.help || `expected /${spec.shape}/`);
  } else {
    add('ok', name, c.dim('set'));
  }
}

// ── 4. optional service reachability ────────────────────────────────────────
if (checkServices && HEALTH_ENDPOINTS.length) {
  for (const url of HEALTH_ENDPOINTS) {
    const code = sh(`curl -s -o /dev/null -w '%{http_code}' --max-time 5 ${url}`);
    if (code === '200') add('ok', `service ${url}`, 'reachable (200)');
    else add('warn', `service ${url}`, code ? `HTTP ${code}` : 'unreachable', `start the app first: ${RUN_COMMAND}`);
  }
}

// ── render ──────────────────────────────────────────────────────────────────
console.log(`\n${c.b(`dev-onboarding doctor`)} — ${PROJECT} · profile: ${c.b(profile)}${CONFIG_PRESENT ? '' : c.dim('  (no dev-onboarding.config.json — using defaults)')}\n`);
for (const r of rows) {
  const icon = r.state === 'ok' ? ICON.ok : r.state === 'warn' ? ICON.warn : ICON.bad;
  console.log(`  ${icon} ${r.label.padEnd(22)} ${r.detail}`);
  if (r.state !== 'ok' && r.fix) console.log(`      ${c.dim('↳ ' + r.fix)}`);
}
const bad = rows.filter((r) => r.state === 'bad');
const warn = rows.filter((r) => r.state === 'warn');
console.log('');
if (bad.length) {
  console.log(c.r(`✗ ${bad.length} blocker(s)`) + (warn.length ? c.y(` · ${warn.length} warning(s)`) : '') + ` — fix the ${ICON.bad} lines above, then re-run.`);
  process.exit(1);
}
console.log(c.g('✓ all required checks passed') + (warn.length ? c.y(` · ${warn.length} warning(s)`) : '') + ` — you're ready: ${c.b(RUN_COMMAND)}`);
