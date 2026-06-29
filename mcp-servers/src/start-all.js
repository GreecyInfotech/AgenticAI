import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const servers = [
  'core-banking.js',
  'crm.js',
  'postgres.js',
  'regulatory.js',
  'email.js',
  'jira.js'
];

console.log('Starting BFSI MCP servers...');

const children = [];

for (const server of servers) {
  const serverPath = join(__dirname, 'servers', server);
  const proc = spawn(process.execPath, [serverPath], { stdio: 'inherit' });
  proc.on('error', (err) => console.error(`Failed to start ${server}:`, err.message));
  children.push(proc);
}

function shutdown() {
  children.forEach(p => p.kill());
  process.exit(0);
}

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
