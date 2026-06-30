// Shared config loader for the dev-onboarding scripts. Reads
// `dev-onboarding.config.json` from the repo root (cwd) so the same scripts drive
// any project; everything below has a sane default if the file is absent.
import fs from 'node:fs';
import path from 'node:path';

const CONFIG_FILE = 'dev-onboarding.config.json';
const cfgPath = path.join(process.cwd(), CONFIG_FILE);
export const CONFIG_PRESENT = fs.existsSync(cfgPath);
const cfg = CONFIG_PRESENT ? JSON.parse(fs.readFileSync(cfgPath, 'utf8')) : {};

export const PROJECT = cfg.project || 'this project';
export const RUN_COMMAND = cfg.runCommand || 'npm start';
export const RUN_URL = cfg.runUrl || null;
export const HEALTH_ENDPOINTS = cfg.healthEndpoints || [];
export const INSTALL_COMMAND = cfg.installCommand || 'npm install';
export const ENV_EXAMPLE = cfg.envExample || '.env.example';
export const ENV_FILE = cfg.envFile || '.env';
/** [{name, range?, versionFrom?, optional?, reason?, installHint?}] */
export const REQUIRED_TOOLS = cfg.requiredTools || [
  { name: 'node' }, { name: 'npm' }, { name: 'git' },
];
/** { NAME: {profiles:[], shape?:regex, mockToggle?, help?, getFrom?} } */
export const SECRETS = cfg.secrets || {};
/** { team:{...}, contributor:{seedCommand?, mockEnv?[], desc?} } */
export const PROFILES = cfg.profiles || { team: {}, contributor: {} };

export function parseProfile(argv, def = 'team') {
  const i = argv.indexOf('--profile');
  const p = i >= 0 ? argv[i + 1] : def;
  return PROFILES[p] ? p : def;
}

/** Secrets that apply to the given profile (defaults to all if no profiles listed). */
export function secretsForProfile(profile) {
  return Object.entries(SECRETS).filter(
    ([, s]) => !s.profiles || s.profiles.includes(profile),
  );
}

// Minimal ANSI helpers (no dep).
export const c = {
  g: (s) => `\x1b[32m${s}\x1b[0m`,
  r: (s) => `\x1b[31m${s}\x1b[0m`,
  y: (s) => `\x1b[33m${s}\x1b[0m`,
  dim: (s) => `\x1b[2m${s}\x1b[0m`,
  b: (s) => `\x1b[1m${s}\x1b[0m`,
};
export const ICON = { ok: '✅', bad: '❌', warn: '⚠️', info: '•' };
