#!/usr/bin/env node
//
// dev-onboarding · scaffold — one-time setup in a target repo. Writes a starter
// `dev-onboarding.config.json` inferred from repo facts (engines, .nvmrc,
// .env.example), appends a labeled "contributor" block to `.env.example`, and
// prints the npm aliases + the prose to drop into the Getting-Started page. The
// generated config is a starting point — review and tune it (mark which secrets
// each profile needs, add seed commands).
//
//   node scaffold.mjs [--force]
//
import fs from 'node:fs';
import { c } from './config.mjs';

const force = process.argv.includes('--force');
const read = (p) => { try { return fs.readFileSync(p, 'utf8'); } catch { return ''; } };
const pkg = (() => { try { return JSON.parse(read('package.json')); } catch { return {}; } })();

// ── infer tools ──────────────────────────────────────────────────────────────
const tools = [];
const nodeRange = fs.existsSync('.nvmrc') ? { name: 'node', versionFrom: '.nvmrc' } : (pkg.engines?.node ? { name: 'node', range: pkg.engines.node } : { name: 'node' });
tools.push(nodeRange);
if (pkg.engines?.npm) tools.push({ name: 'npm', range: pkg.engines.npm }); else tools.push({ name: 'npm' });
tools.push({ name: 'git' });
if (/docker/.test(JSON.stringify(pkg.scripts || {}))) tools.push({ name: 'docker', optional: true, reason: 'local services (e.g. Redis)' });

// ── infer secrets from .env.example ──────────────────────────────────────────
const envEx = read('.env.example');
const secrets = {};
for (const m of envEx.matchAll(/^\s*([A-Z][A-Z0-9_]+)\s*=/gm)) {
  const k = m[1];
  if (/(KEY|SECRET|TOKEN|PASSWORD|DATABASE_URL|_URL|DSN)$/.test(k) && !/^VITE_|^NEXT_PUBLIC_|PORT$|HOST$/.test(k)) {
    secrets[k] = { profiles: ['team', 'contributor'], help: `set ${k}` };
  }
}

const runCommand = pkg.scripts?.start ? 'npm start' : pkg.scripts?.dev ? 'npm run dev' : 'npm start';
const config = {
  project: pkg.name || 'this project',
  runCommand,
  runUrl: null,
  healthEndpoints: [],
  installCommand: 'npm install',
  envExample: '.env.example',
  envFile: '.env',
  requiredTools: tools,
  secrets,
  profiles: {
    team: { desc: 'internal access to the real backing services' },
    contributor: { desc: 'own free-tier accounts / seed data — no internal access', seedCommand: null, mockEnv: [] },
  },
};

// ── write config ─────────────────────────────────────────────────────────────
const CFG = 'dev-onboarding.config.json';
if (fs.existsSync(CFG) && !force) {
  console.log(c.y(`${CFG} already exists — not overwriting (use --force).`));
} else {
  fs.writeFileSync(CFG, JSON.stringify(config, null, 2) + '\n');
  console.log(c.g(`✓ wrote ${CFG}`) + c.dim(` (${Object.keys(secrets).length} secrets, ${tools.length} tools inferred — review it)`));
}

// ── append contributor block to .env.example ─────────────────────────────────
const MARK = '# ── Contributor (no internal access) ──';
if (envEx && !envEx.includes(MARK) && fs.existsSync('.env.example')) {
  const block = `\n${MARK}\n` +
    `# Forking to customize or contribute? You don't need internal access. Use your own\n` +
    `# free-tier accounts and (optionally) seed/mocks. Document the toggles here, e.g.:\n` +
    `#   USE_SEED_DATA=true        # serve seeded sample data instead of live internal data\n` +
    `#   USE_MOCK_WEATHER=true     # skip the weather API key (clearly-labeled, not silent)\n`;
  fs.appendFileSync('.env.example', block);
  console.log(c.g('✓ appended a "Contributor (no internal access)" block to .env.example'));
}

// ── print next steps ─────────────────────────────────────────────────────────
console.log(`\n${c.b('Next:')}`);
console.log(`  1. Review ${CFG} — set each secret's profiles, shapes, and a contributor seed command.`);
console.log(`  2. Add npm aliases:`);
console.log(c.dim(`       "doctor":    "node ~/.claude/skills/dev-onboarding/scripts/doctor.mjs",`));
console.log(c.dim(`       "bootstrap": "node ~/.claude/skills/dev-onboarding/scripts/bootstrap.mjs"`));
console.log(`  3. Point the Getting-Started page at \`npm run doctor\` / \`npm run bootstrap\`.`);
