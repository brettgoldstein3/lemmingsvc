"""Build index.html for the v4 cut: 3 roast lines → "Introducing VCs…" → action lines → "Play it for free".
Every cut and caption lands on a word, from the VO character timestamps (assets/vo4/timing.json)."""
import json, os, subprocess

ROOT = os.path.join(os.path.dirname(__file__), '..')
T = json.load(open(os.path.join(ROOT, 'assets/vo4/timing.json')))
RATE = 1.05                     # VO playback rate (pitch-preserved)
GAP = 0.1                       # breath between lines: no dead air
r2 = lambda x: round(x, 3)
R1_RATE = 0.85                  # stretch the cliff shot to cover the single roast line

# ---- VO schedule: lines back to back ----
ORDER = ['r1', 'intro', 'a1', 'a2', 'cta']
VO = {}
t = 0.25
for k in ORDER:
    VO[k] = r2(t)
    t += T[k]['duration'] / RATE + GAP
mark = lambda k, m: r2(VO[k] + T[k]['marks'][m] / RATE)
END = r2(VO['cta'] - 0.05)       # end card lands just before "Play it for free"
TOTAL = r2(END + 3.0)

# ---- picture: (id, clip, start, end, media-start, rate) ----
SHOTS = [
    ('r1', 'b-follow', 0.3, VO['intro'], 0.0, R1_RATE),
    ('a1a', 'a-lead', VO['a1'], mark('a1', 'the burn rate'), 0.5, 1),
    ('a1b', 'd-burn2', mark('a1', 'the burn rate'), mark('a1', 'Demo Day'), 0.3, 1),
    ('a1c', 'v3-demoday', mark('a1', 'Demo Day'), VO['a2'], 2.0, 1),
    ('dig', 'c-curve2', VO['a2'], mark('a2', 'Build'), 0.3, 1),
    ('build', 'e-series', mark('a2', 'Build'), mark('a2', 'Bash'), 0.1, 1),
    ('bash', 'v4-bash', mark('a2', 'Bash'), mark('a2', 'Block'), 0.2, 1),
    ('block', 'v4-block', mark('a2', 'Block'), mark('a2', 'Get every'), 0.5, 1),
    ('every', 'g-exit', mark('a2', 'Get every'), None, 0.3, 1),   # ends where the result card starts
]
RESULT = (r2(mark('a2', 'Get every') + 1.5), END)
SHOTS[-1] = SHOTS[-1][:3] + (RESULT[0],) + SHOTS[-1][4:]

# ---- captions: row A (setup, VT323 white) / row B (punch, Press Start green) ----
def fit_punch(txt, mx=40):
    return min(mx, 1000 // len(txt))
CAPS = []  # (id, row, text, start, end, size, entrance)
def cap(cid, row, text, start, end, size=None, ent='slam'):
    CAPS.append((cid, row, text, r2(start), r2(end), size, ent))

roasts = [('r1', 'THIS IS A GAME FOR BOLD, INDEPENDENT INVESTORS...', 'WHO ASK WHO ELSE IS IN.', 'who ask')]
nxt = {'r1': VO['intro']}
for k, setup, punch, m in roasts:
    cap(f'{k}-a', 'A', setup, VO[k], nxt[k], None, 'drop')
    cap(f'{k}-b', 'B', punch, mark(k, m), nxt[k], fit_punch(punch, 34), 'slam')
cap('in-a', 'A', 'INTRODUCING...', VO['intro'], VO['a1'], None, 'drop')
cap('in-b', 'B', 'VCs.', mark('intro', 'V.C.s'), VO['a1'], 64, 'slam')
cap('a1-a', 'A', 'LEAD THE HERD THROUGH...', VO['a1'], VO['a2'], None, 'drop')
cap('a1-b1', 'B', 'THE DATA ROOM,', mark('a1', 'the data room'), mark('a1', 'the burn rate'), 40, 'snapL')
cap('a1-b2', 'B', 'THE BURN RATE,', mark('a1', 'the burn rate'), mark('a1', 'Demo Day'), 40, 'snapR')
cap('a1-b3', 'B', 'AND DEMO DAY.', mark('a1', 'Demo Day'), VO['a2'], 40, 'snapL')
verbs = [('DIG.', VO['a2'], mark('a2', 'Build')), ('BUILD.', mark('a2', 'Build'), mark('a2', 'Bash')),
         ('BASH.', mark('a2', 'Bash'), mark('a2', 'Block')), ('BLOCK.', mark('a2', 'Block'), mark('a2', 'Get every'))]
for i, (w, s, e) in enumerate(verbs):
    cap(f'v{i}', 'V', w, s, e, 88, 'slam')
cap('ev-a', 'A', 'GET EVERY VC...', mark('a2', 'Get every'), END, None, 'drop')
cap('ev-b', 'B', 'INTO THE ROUND.', mark('a2', 'Get every') + 0.5, END, 40, 'slam')

old = open(os.path.join(ROOT, 'tools/index-v3.html')).read()  # clean base styles (keeps rebuilds idempotent)
style = old[old.index('<style>'):old.index('</style>') + len('</style>')]
style = style.replace('</style>', '''      .verb { position: absolute; left: 0; top: 40px; width: 1080px; height: 150px; display: flex; align-items: center; justify-content: center; }
      .verb .t { display: block; font-family: "Press Start 2P", monospace; line-height: 1; color: #7cf06a; text-shadow: 7px 7px 0 #000; white-space: nowrap; will-change: transform; }
      #intro-dirt { position: absolute; inset: 0; background: url("assets/dirt.png") 0 0 / 960px auto repeat; }
      #intro-shade { position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0.05), rgba(0,0,0,0.6)); }
      #sh { position: absolute; left: 0; top: 512px; width: 960px; height: 88px; overflow: hidden; }
      #sh .vc { bottom: 8px; }
      #sh-ground { position: absolute; left: 0; right: 0; bottom: 0; height: 10px; background: #58c850; box-shadow: inset 0 3px 0 #8ae07a; }
      #cta-pill { font-size: 25px !important; gap: 18px !important; padding: 20px 24px 18px !important; }
      #cta-pill small { font-size: 16px !important; }
      #intro-sub { position: absolute; left: 0; top: 462px; width: 960px; height: 40px; display: flex; justify-content: center; }
      #intro-sub span { display: block; font-family: "Press Start 2P", monospace; font-size: 20px; color: #f0d8a0; text-shadow: 3px 3px 0 #000; }
    </style>''')

cap_html, tl = [], []
ENT = {
    'drop': ('{ y: -40, opacity: 0 }', '{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }'),
    'slam': ('{ scale: 1.9, filter: "blur(12px)", opacity: 0 }', '{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.28, ease: "power4.out" }'),
    'snapL': ('{ x: -420, opacity: 0 }', '{ x: 0, opacity: 1, duration: 0.25, ease: "expo.out" }'),
    'snapR': ('{ x: 420, opacity: 0 }', '{ x: 0, opacity: 1, duration: 0.25, ease: "expo.out" }'),
}
for cid, row, text, s, e, size, ent in CAPS:
    cls = {'A': 'setup', 'B': 'punch', 'V': 'verb'}[row]
    fs = size or min(50, int(1900 / len(text)))
    cap_html.append(f'      <div id="c-{cid}" class="{cls} clip" data-start="{s}" data-duration="{r2(e - s)}" data-track-index="1"><span class="t" style="font-size:{fs}px">{text}</span></div>')
    f, to = ENT[ent]
    tl.append(f'      tl.fromTo("#c-{cid} .t", {f}, {to}, {s});')
# setups dim when their punchline lands
for k, *_ in roasts:
    tl.append(f'      tl.fromTo("#c-{k}-a .t", {{ opacity: 1 }}, {{ opacity: 0.55, duration: 0.2, immediateRender: false }}, {mark(k, roasts[[x[0] for x in roasts].index(k)][3])});')

vid_html = []
for sid, clip, s, e, ms, rate in SHOTS:
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1 else ''
    vid_html.append(f'          <video id="v-{sid}" src="assets/clips/{clip}.mp4" data-start="{r2(s)}" data-duration="{r2(e - s)}" data-media-start="{ms}"{rate_attr} data-track-index="3" muted playsinline></video>')
CUTS = sorted({r2(s[2]) for s in SHOTS} | {VO['intro'], RESULT[0], END})

def fdur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, f)]).decode())
audio = [f'      <audio id="a-music" src="assets/audio/music-v5.wav" data-start="0" data-duration="{TOTAL}" data-volume="1.0" data-track-index="10"></audio>']
for k in ORDER:
    audio.append(f'      <audio id="a-vo-{k}" src="assets/vo4/{k}.mp3" data-start="{VO[k]}" data-duration="{r2(T[k]["duration"] / RATE - 0.005)}" data-playback-rate="{RATE}" data-track-index="11"></audio>')
sfx = [('a-crt', 'crt-on.wav', 0.0, 0.3), ('a-splat1', 'splat.wav', r2(0.3 + 2.04 / R1_RATE), 0.22), ('a-splat2', 'splat.wav', r2(0.3 + 3.66 / R1_RATE), 0.22),
       ('a-slam1', 'slam.wav', mark('intro', 'V.C.s'), 0.18), ('a-slam2', 'slam.wav', END, 0.18)]
for i, (k, *_r) in enumerate(roasts):
    sfx.append((f'a-hit{i}', 'blip.wav', mark(k, roasts[i][3]), 0.16))
for i, (_w, s, _e) in enumerate(verbs):
    sfx.append((f'a-verb{i}', 'blip.wav', r2(s), 0.14))
for i, (aid, f, st, vol) in enumerate(sfx):
    audio.append(f'      <audio id="{aid}" src="assets/audio/{f}" data-start="{st}" data-duration="{r2(fdur("assets/audio/" + f) - 0.005)}" data-volume="{vol}" data-track-index="{12 + i % 4}"></audio>')

LOGO = mark('intro', 'V.C.s'); ADAPT = mark('intro', 'An adaptation')
html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    {style}
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1080" data-fps="30">
      <div id="bg"></div>
      <div id="bg-shade"></div>

      <!-- captions, each timed to its word -->
{chr(10).join(cap_html)}
      <div id="cap-end" class="cap clip" data-start="{END}" data-duration="{r2(TOTAL - END)}" data-track-index="1"><span class="t">LEMMINGS, BUT THEY'RE <em>VCs.</em></span></div>

      <!-- the computer -->
      <div id="monitor">
        <div id="bezel"></div>
        <div id="tube-frame"></div>
        <div id="screen">
{chr(10).join(vid_html)}
          <div id="s-result" class="layer result-crop clip" data-start="{RESULT[0]}" data-duration="{r2(RESULT[1] - RESULT[0])}" data-track-index="2"><img src="assets/clips/h-result.png" alt="" /></div>
          <!-- reveal: "Introducing… VCs" -->
          <div id="s-intro" class="layer clip" data-start="{VO['intro']}" data-duration="{r2(VO['a1'] - VO['intro'])}" data-track-index="2">
            <div id="intro-dirt"></div>
            <div id="intro-shade"></div>
            <div id="sh" data-layout-allow-overflow><div id="sh-ground"></div>
              <div class="vc shv" id="sh0"><img src="assets/badge-a16z.png" alt="" style="width:40px;height:18px;margin-left:-20px" /></div>
              <div class="vc shv" id="sh1"></div><div class="vc shv" id="sh2"></div><div class="vc shv" id="sh3"></div><div class="vc shv" id="sh4"></div><div class="vc shv" id="sh5"></div><div class="vc shv" id="sh6"></div>
            </div>
            <div id="logo-stack">
              <img class="ghost warm" src="assets/logo.png" alt="" />
              <img class="ghost cool" src="assets/logo.png" alt="" />
              <img id="logo-base" src="assets/logo.png" alt="VCs" />
            </div>
            <div id="intro-sub"><span id="intro-sub-t">AN ADAPTATION OF THE 1990s CLASSIC, LEMMINGS</span></div>
          </div>
          <div id="end-screen" class="layer clip" data-start="{END}" data-duration="{r2(TOTAL - END)}" data-track-index="2">
            <div id="end-shade"></div>
            <img id="end-logo" src="assets/logo.png" alt="VCs" />
            <div id="press" data-layout-allow-occlusion><span id="press-t" data-layout-allow-occlusion>▶ PRESS START</span></div>
          </div>
          <!-- CRT power-on over the first shot -->
          <div id="s0" class="layer clip" data-start="0" data-duration="0.45" data-track-index="2"><div id="crt-line"></div></div>
          <div id="flash"></div>
          <div id="glass" data-layout-allow-occlusion></div>
        </div>
        <div id="chin">
          <div id="brand"><div id="stripes"><i style="background:#58b848"></i><i style="background:#f0c030"></i><i style="background:#e8742a"></i><i style="background:#d8402a"></i><i style="background:#8a4ab8"></i><i style="background:#3a8ad0"></i></div>VC-1991</div>
          <div id="grille"></div>
          <div id="knobs"><i></i><i></i><span id="led"></span></div>
        </div>
      </div>

      <!-- bottom: persistent CTA line, then the big button -->
      <div id="url-line" class="clip" data-start="0.3" data-duration="{r2(END - 0.3)}" data-track-index="4"><span id="url-t">▶ PLAY FREE · <b>lemmingsvc.vercel.app</b></span></div>
      <div id="cta" class="clip" data-start="{END}" data-duration="{r2(TOTAL - END)}" data-track-index="4">
        <div id="cta-pill">▶ PLAY IT FOR FREE <small>lemmingsvc.vercel.app</small></div>
      </div>
      <div id="herd" data-layout-allow-overflow class="clip" data-start="{END}" data-duration="{r2(TOTAL - END)}" data-track-index="5">
        <div class="vc" id="vc0"><img src="assets/badge-sequoia.png" alt="" /></div>
        <div class="vc" id="vc1"></div><div class="vc" id="vc2"></div><div class="vc" id="vc3"></div>
        <div class="vc" id="vc4"></div><div class="vc" id="vc5"></div><div class="vc" id="vc6"></div><div class="vc" id="vc7"></div>
      </div>

      <!-- audio: score, VO (ElevenLabs "Adam", eleven_v3, {RATE}x), quiet SFX -->
{chr(10).join(audio)}
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const hash = (n) => {{ const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }};

      // CRT power-on over the first shot
      tl.fromTo("#crt-line", {{ scaleX: 0.02, scaleY: 1, opacity: 1 }}, {{ scaleX: 1, duration: 0.1, ease: "expo.out" }}, 0.02);
      tl.to("#crt-line", {{ scaleY: 150, opacity: 0, duration: 0.2, ease: "power2.in" }}, 0.14);

      // reveal: static, then the logo slams on "VCs" with an RGB-split glitch + monitor shake, title-screen dirt behind
      const shv = gsap.utils.toArray("#sh .shv");
      const sh = {{ p: 0 }};
      tl.fromTo(sh, {{ p: 0 }}, {{ p: 1, duration: {r2(VO['a1'] - VO['intro'] - 0.05)}, ease: "none",
        onUpdate: () => {{ const f = Math.floor(tl.time() / 0.07) % 8;
          shv.forEach((el, i) => {{ gsap.set(el, {{ x: -40 + sh.p * 1100 - i * 48 - (i > 2 ? 16 : 0), backgroundPosition: `${{-((f + i * 3) % 8) * 36}}px 0px` }}); }}); }} }}, {VO['intro']});
      tl.fromTo("#logo-stack", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.28, ease: "power4.out" }}, {LOGO});
      const ghosts = gsap.utils.toArray("#logo-stack .ghost");
      const amp = {{ a: 0 }};
      tl.set(ghosts, {{ opacity: 0.8 }}, {LOGO});
      tl.fromTo(amp, {{ a: 1 }}, {{ a: 0, duration: 0.45, ease: "power3.in", immediateRender: false,
        onUpdate: () => {{ const step = Math.floor(tl.time() / 0.04);
          ghosts.forEach((el, i) => gsap.set(el, {{ x: (hash(step * 13 + i * 7) * 2 - 1) * 26 * amp.a, y: (hash(step * 29 + i * 11) * 2 - 1) * 8 * amp.a }})); }} }}, {LOGO});
      tl.set(ghosts, {{ opacity: 0, x: 0, y: 0 }}, {r2(LOGO + 0.46)});
      const shake = {{ a: 0 }};
      tl.fromTo(shake, {{ a: 1 }}, {{ a: 0, duration: 0.35, ease: "power2.in", immediateRender: false,
        onUpdate: () => {{ const s = Math.floor(tl.time() / 0.035); gsap.set("#monitor", {{ x: (hash(s) * 2 - 1) * 12 * shake.a, y: (hash(s + 50) * 2 - 1) * 8 * shake.a }}); }} }}, {LOGO});
      tl.set("#monitor", {{ x: 0, y: 0 }}, {r2(LOGO + 0.36)});
      tl.fromTo("#intro-sub-t", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {ADAPT});

      // captions
{chr(10).join(tl)}

      // hard-cut flashes
      {json.dumps(CUTS)}.forEach((t) => {{
        tl.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.12, ease: "power2.out", immediateRender: false }}, t);
      }});
      tl.fromTo("#url-t", {{ opacity: 0, y: 12 }}, {{ opacity: 0.9, y: 0, duration: 0.4, ease: "power2.out" }}, 0.5);

      // end card
      tl.fromTo("#cap-end .t", {{ scale: 1.8, filter: "blur(16px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.4, ease: "power4.out" }}, {END});
      tl.fromTo("#end-logo", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }}, {END});
      tl.fromTo("#press-t", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, {r2(END + 0.5)});
      tl.to("#press-t", {{ opacity: 0.1, duration: 0.01, yoyo: true, repeat: Math.max(0, Math.floor(2.2 / 0.5) - 1), repeatDelay: 0.24 }}, {r2(END + 0.75)});
      tl.fromTo("#cta-pill", {{ y: 140, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "circ.out" }}, {END});
      tl.to("#cta-pill", {{ scale: 1.05, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(2.4 / 0.7) - 1) }}, {r2(END + 0.5)});
      const vcs = gsap.utils.toArray("#herd .vc");
      const herd = {{ p: 0 }};
      tl.fromTo(herd, {{ p: 0 }}, {{ p: 1, duration: {r2(TOTAL - END - 0.1)}, ease: "none",
        onUpdate: () => {{ const f = Math.floor(tl.time() / 0.07) % 8;
          vcs.forEach((el, i) => {{ const x = 120 + herd.p * 900 - i * 52 - (i > 3 ? 18 : 0) + 240;
            gsap.set(el, {{ x, backgroundPosition: `${{-((f + i * 3) % 8) * 36}}px 0px` }}); }}); }} }}, {r2(END + 0.05)});

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w').write(html)
print('built v4', 'total', TOTAL, 'end', END)
print({k: v for k, v in VO.items()})
