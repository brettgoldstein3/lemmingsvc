// Regression tests. On /play/, in the browser console: await import('./tests.js').then(m => m.run())
// PLANS[i] is a scripted solution for level i: called once per tick with the game state.
const V = () => window.__vcs;
const A = (v, s) => V().assign(v, s);

export const PLANS = {
  0: G => { const v = G.vcs[0]; if (v && v.act === 'walk' && v.x >= 200 && !G._d) G._d = A(v, 'digger'); },
  1: G => { for (const v of G.vcs) if (v.alive && !v.float) A(v, 'floater'); },
  2: G => {
    const a = G.vcs[0], b = G.vcs[1];
    if (a && a.alive && a.act === 'walk' && a.x >= 226 && a.dir > 0 && !G._b0) G._b0 = A(a, 'builder');
    if (a && a.alive && G._b0 && a.act === 'shrug' && a.x < 320) A(a, 'builder');
    if (b && b.alive && b.act === 'walk' && b.x >= 150 && !G._bl) G._bl = A(b, 'blocker');
    if (G._bl && !G._bomb && a && (a.x >= 320 || !a.alive)) G._bomb = A(b, 'bomber');
  },
  3: G => {
    G._w = G._w || {};
    for (const v of G.vcs) { if (!v.alive || v.act !== 'walk' || v.dir < 0) continue;
      for (const wx of [200, 340, 480]) if (!G._w[wx] && v.x >= wx - 4 && v.x < wx && A(v, 'basher')) G._w[wx] = 1; }
  },
  4: G => {
    for (const v of G.vcs) { if (!v.alive) continue;
      if (!G._dig && v.act === 'walk' && v.dir > 0 && v.y < 80 && v.x >= 225) { G._dig = A(v, 'digger'); continue; }
      if (G._dig && !G._blk && v.act === 'walk' && v.y < 80 && v.x >= 270 && v.dir > 0) { G._blk = A(v, 'blocker'); continue; }
      if (!G._blk2 && v.act === 'walk' && v.y > 100 && v.y < 115 && v.x <= 192 && v.dir < 0) { G._blk2 = A(v, 'blocker'); continue; }
      if (!G._bash && v.act === 'walk' && v.y > 130 && v.x >= 414 && v.x < 420 && v.dir > 0) G._bash = A(v, 'basher');
    }
  },
  5: G => {
    const a = G.vcs[0];
    if (a && a.alive) {
      if (!G._dig && a.act === 'walk' && a.x >= 100) G._dig = A(a, 'digger');
      if (G._dig && !G._bash && a.act === 'dig' && a.y >= 124) G._bash = A(a, 'basher');
      if (G._bash && !G._build && a.act === 'walk' && a.dir > 0 && a.x >= 187 && a.x < 192) G._build = A(a, 'builder');
    }
    if (G._build && !G._blk) { const b = G.vcs.find(v => v !== a && v.alive && v.act === 'walk' && v.dir > 0 && v.x >= 165 && v.x <= 178 && v.y > 120); if (b) { G._blk = b; A(b, 'blocker'); } }
    if (G._blk && !G._bomb && a && (a.x >= 216 || !a.alive) && a.act !== 'build') G._bomb = A(G._blk, 'bomber');
  },
  6: G => {
    const a = G.vcs[0];
    if (a && a.alive) {
      if (!G._b && a.act === 'walk' && a.dir > 0 && a.x >= 326 && a.y > 125) G._b = A(a, 'builder');
      else if (G._b && a.act === 'shrug' && a.x < 400) A(a, 'builder');
    }
    if (G._b && !G._blk) { const b = G.vcs.find(v => v !== a && v.alive && v.act === 'walk' && v.dir > 0 && v.x >= 290 && v.x <= 310 && v.y > 125); if (b) { G._blk = b; A(b, 'blocker'); } }
    if (G._blk && !G._bomb && a && (!a.alive || (a.x >= 395 && a.act === 'walk'))) G._bomb = A(G._blk, 'bomber');
    if (!G._bash) { const v = G.vcs.find(v => v.alive && v.act === 'walk' && v.dir > 0 && v.x >= 476 && v.x < 480); if (v) G._bash = A(v, 'basher'); }
  },
  7: G => {
    const a = G.vcs[0]; if (!a || !a.alive) return;
    for (const [sx, sy, n] of [[48, 130, 2], [128, 112, 2], [208, 94, 2], [292, 76, 3]])
      if (a.act === 'walk' && a.dir > 0 && a.x >= sx && a.x < sx + 3 && Math.abs(a.y - sy) < 3 && !G['s' + sx]) { G['s' + sx] = n - 1; G._cur = sx; A(a, 'builder'); }
    if (a.act === 'shrug' && G._cur != null && G['s' + G._cur] > 0) { A(a, 'builder'); G['s' + G._cur]--; }
    if (a.x >= 294 && !G._blk) { const b = G.vcs.find(v => v !== a && v.alive && v.act === 'walk' && v.dir > 0 && v.x >= 274 && v.x < 284 && v.y < 80); if (b) { G._blk = b; A(b, 'blocker'); } }
    if (G._blk && !G._bomb && a.x >= 360 && a.act === 'walk') G._bomb = A(G._blk, 'bomber');
  },
  8: G => {
    const r = G.vcs[1];
    if (r && !G._br && r.alive && r.act === 'walk' && r.dir > 0 && r.x >= 596) G._br = A(r, 'blocker');
    if (!G._bl) { const v = G.vcs.find(v => v.alive && v.act === 'walk' && v.dir < 0 && v.x <= 44); if (v) G._bl = A(v, 'blocker'); }
    if (!G._lb) { const v = G.vcs.find(v => v.alive && v.act === 'walk' && v.dir > 0 && v.x >= 224 && v.x <= 228 && v.y > 125); if (v) { G._lb = v; A(v, 'builder'); } }
    else if (G._lb.act === 'shrug' && !G._lb2) G._lb2 = A(G._lb, 'builder');
    if (!G._rb) { const v = G.vcs.find(v => v.alive && v.act === 'walk' && v.dir < 0 && v.x >= 412 && v.x <= 416 && v.y > 125); if (v) { G._rb = v; A(v, 'builder'); } }
    else if (G._rb.act === 'shrug' && !G._rb2) G._rb2 = A(G._rb, 'builder');
  }
};

export function run() {
  const out = {}, saved = localStorage.getItem('vcs_unlocked');
  const play = (i, plan, maxT = 8000) => {
    V().startLevel(i); V().S = 'play'; const G = V().G; let t = 0;
    while (V().S === 'play' && t < maxT) { plan(G, t); V().tick(); t++; }
    return { won: !!G.won, pct: G.pct, t };
  };
  const expect = (name, r, won) => { out[name] = (r.won === won ? 'PASS' : 'FAIL') + ` (${r.pct}%, ${r.t} ticks)`; };
  for (let i = 0; i < V().LEVELS.length; i++) expect('L' + (i + 1) + ' idle loses', play(i, () => {}), false);
  for (let i = 0; i < V().LEVELS.length; i++) if (PLANS[i]) expect('L' + (i + 1) + ' solved', play(i, PLANS[i]), true);
  V().startLevel(0); V().S = 'title';
  if (saved === null) localStorage.removeItem('vcs_unlocked'); else localStorage.setItem('vcs_unlocked', saved);
  return out;
}
