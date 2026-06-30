#!/usr/bin/env node
//
// dev-onboarding · bootstrap — IDEMPOTENT setup: tools check → install → .env →
// profile-specific data path → hand off to the run command. Re-runnable: skips
// what's already done. The deterministic counterpart to the agent, which
// diagnoses/adapts; this just does the reproducible steps.
//
//   node bootstrap.mjs [--profile team|contributor] [--force]
//
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  PROJECT, RUN_COMMAND, INSTALL_COMMAND, ENV_EXAMPLE, ENV_FILE, PROFILES,
  parseProfile, c,
} from './config.mjs';

const argv = process.argv.slice(2);
const profile = parseProfile(argv, 'team');
const force = argv.includes('--force');
const run = (cmd, opts = {}) => execSync(cmd, { stdio: 'inherit', ...opts });
const step = (s) => console.log(`\n${c.b('▸ ' + s)}`);

console.log(`${c.b('dev-onboarding bootstrap')} — ${PROJECT} · profile: ${c.b(profile)}`);
const prof = PROFILES[profile] || {};

// 1. Tools & env (read-only doctor; warn but continue so install can still proceed).
step('Checking tools & env');
const here = path.dirname(fileURLToPath(import.meta.url));
try {
  run(`node "${path.join(here, 'doctor.mjs')}" --profile ${profile}`);
} catch {
  console.log(c.y(`  ↑ blockers above — deps will still install, but fix them before \`${RUN_COMMAND}\`.`));
}

// 2. Dependencies (idempotent).
step('Installing dependencies');
if (force || !fs.existsSync('node_modules')) run(INSTALL_COMMAND);
else console.log(c.dim('  node_modules present — skipping (use --force to reinstall)'));

// 3. .env (idempotent — never overwrite an existing one).
step('Environment file');
if (!fs.existsSync(ENV_FILE)) {
  fs.copyFileSync(ENV_EXAMPLE, ENV_FILE);
  console.log(`  created ${ENV_FILE} from ${ENV_EXAMPLE} ${c.y('— fill in the secrets (see doctor output)')}`);
} else {
  console.log(c.dim(`  ${ENV_FILE} present — leaving it untouched`));
}

// 4. Profile-specific data path.
if (profile === 'contributor') {
  step('Contributor data path (your own free-tier accounts — no internal access)');
  if (prof.mockEnv?.length) {
    let env = fs.readFileSync(ENV_FILE, 'utf8');
    let added = [];
    for (const kv of prof.mockEnv) {
      const [k] = kv.split('=');
      if (!new RegExp(`^\\s*${k}\\s*=`, 'm').test(env)) { env += `\n${kv}\n`; added.push(kv); }
    }
    if (added.length) { fs.writeFileSync(ENV_FILE, env); console.log(`  added toggles: ${added.join(', ')}`); }
  }
  if (prof.seedCommand) {
    console.log(`  load sample data into your own DB:  ${c.b(prof.seedCommand)}`);
    console.log(c.dim('  (point DATABASE_URL at your free Neon dev branch first — real data, not silent mocks)'));
  }
} else {
  step('Team data path (internal access)');
  console.log('  fill .env with your internal Neon dev-branch URL + OpenWeather key, then verify with the doctor.');
}

// 5. Done.
step('Next step');
console.log(`  ${c.g('✓')} bootstrap complete. Start the app:  ${c.b(RUN_COMMAND)}`);
console.log(c.dim(`  re-run the doctor anytime to verify your environment (e.g. \`npm run doctor\`).`));
