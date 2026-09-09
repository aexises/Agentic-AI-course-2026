// Compatibility entry point: the textbook now uses authored Markdown sources.
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const script = fileURLToPath(new URL('./build-textbook.py', import.meta.url));
const result = spawnSync(process.env.PYTHON || 'python3', [script, ...process.argv.slice(2)], { stdio: 'inherit' });
if (result.error) throw result.error;
process.exitCode = result.status ?? 1;
