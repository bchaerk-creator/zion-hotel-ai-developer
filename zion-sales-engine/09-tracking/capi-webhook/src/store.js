'use strict';
// Idempotencia. Guarda SO chave de evento, status e hora. Nenhum dado pessoal.
const fs = require('node:fs');
const path = require('node:path');

function createStore(spec) {
  const map = new Map();
  let file = null;
  if (spec && spec !== 'memory') {
    file = path.resolve(spec);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    if (fs.existsSync(file)) {
      for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
        if (!line.trim()) continue;
        try { const r = JSON.parse(line); map.set(r.k, r.s); } catch (_) { /* linha corrompida: ignora */ }
      }
    }
  }
  return {
    get(key) { return map.get(key); },
    set(key, status) {
      map.set(key, status);
      if (file) fs.appendFileSync(file, JSON.stringify({ k: key, s: status, t: new Date().toISOString() }) + '\n');
    },
    size() { return map.size; },
  };
}

module.exports = { createStore };
