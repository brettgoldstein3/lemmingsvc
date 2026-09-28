"""Build index.html for the v3 'This game is for…' cut from the VO timestamps (assets/vo3/timing.json)."""
import json, os, re, subprocess
ROOT = os.path.join(os.path.dirname(__file__), '..')
T = json.load(open(os.path.join(ROOT, 'assets/vo3/timing.json')))
RATE = 1.08
old = open(os.path.join(ROOT, 'index.html')).read()
style = old[old.index('<style>'):old.index('</style>') + len('</style>')]
style = style.replace('</style>', '''      /* v3: two-line roast captions — setup (VT323) + punchline (Press Start, green) */
      .setup { position: absolute; left: 0; top: 34px; width: 1080px; height: 70px; display: flex; align-items: center; justify-content: center; }
      .setup .t { display: block; font-family: "VT323", monospace; font-size: 50px; line-height: 1; color: #fff; text-shadow: 4px 4px 0 #000; white-space: nowrap; will-change: transform; }
      .punch { position: absolute; left: 0; top: 112px; width: 1080px; height: 80px; display: flex; align-items: center; justify-content: center; }
      .punch .t { display: block; font-family: "Press Start 2P", monospace; line-height: 1.2; color: #7cf06a; text-shadow: 5px 5px 0 #000; white-space: nowrap; will-change: transform; }
    </style>''')

# (id, setup, punchline, clip, clip media-start, vo id)
SEGS = [
    ('s1', 'THIS GAME IS FOR CONTRARIAN INVESTORS...', "WHO ASK WHO ELSE IS IN.", 'b-follow', 0.3, 'l1'),
    ('s2', 'FOR EARLY BELIEVERS...', "WHO ASK IF THERE'S ALLOCATION LATER.", 'v3-party', 0.1, 'l2'),
    ('s3', 'FOR CONVICTION-DRIVEN FUNDS...', 'THAT JUST NEED A LEAD FIRST.', 'v3-demoday', 0.1, 'l3'),
    ('s4', 'FOR THESIS-DRIVEN FIRMS...', "WHOSE THESIS IS: WHATEVER'S HOT.", 'v3-hype', 0.05, 'l4'),
    ('s5', 'FOR FOUNDER-FRIENDLY PARTNERS...', "WHO'LL CIRCLE BACK AFTER TRACTION.", 'v3-circle', 0.2, 'l5'),
    ('s6', 'FOR BOLD, INDEPENDENT THINKERS...', 'WHO DO WHATEVER SEQUOIA DOES.', 'v3-sequoia', 0.1, 'l6'),
]
VO_START = {'l1': 0.9, 'l2': 5.8, 'l3': 10.3, 'l4': 15.1, 'l5': 21.0, 'l6': 25.9, 'end': 31.7}
CUTS = [2.2, 5.8, 10.3, 15.1, 21.0, 25.9, 31.5]
TOTAL = 38.4
r2 = lambda x: round(x, 3)

caps, vids, tl, flashes = [], [], [], []
for i, (sid, setup, punch, clip, ms, vo) in enumerate(SEGS):
    seg0, seg1 = CUTS[i], CUTS[i + 1]
    setup_t = VO_START[vo] if i == 0 else seg0  # line 1's setup is spoken over the logo
    punch_t = r2(VO_START[vo] + T[vo]['punch'] / RATE)
    psize = min(34, 1000 // len(punch)); ssize = min(50, int(1900 / len(setup)))
    caps.append(f'      <div id="{sid}-a" class="setup clip" data-start="{r2(setup_t)}" data-duration="{r2(seg1 - setup_t)}" data-track-index="1"><span class="t" style="font-size:{ssize}px">{setup}</span></div>')
    caps.append(f'      <div id="{sid}-b" class="punch clip" data-start="{punch_t}" data-duration="{r2(seg1 - punch_t)}" data-track-index="1"><span class="t" style="font-size:{psize}px">{punch}</span></div>')
    vids.append(f'          <video id="v-{sid}" src="assets/clips/{clip}.mp4" data-start="{seg0}" data-duration="{r2(seg1 - seg0)}" data-media-start="{ms}" data-track-index="3" muted playsinline></video>')
    entr = [('{ y: -40, opacity: 0 }', '{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }'),
            ('{ x: -300, opacity: 0 }', '{ x: 0, opacity: 1, duration: 0.35, ease: "expo.out" }'),
            ('{ x: 300, opacity: 0 }', '{ x: 0, opacity: 1, duration: 0.35, ease: "expo.out" }')][i % 3]
    tl.append(f'      tl.fromTo("#{sid}-a .t", {entr[0]}, {entr[1]}, {r2(setup_t)});')
    tl.append(f'      tl.fromTo("#{sid}-b .t", {{ scale: 1.9, filter: "blur(12px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.32, ease: "power4.out" }}, {punch_t});')
    tl.append(f'      tl.fromTo("#{sid}-a .t", {{ opacity: 1 }}, {{ opacity: 0.55, duration: 0.25, immediateRender: false }}, {punch_t});')
    flashes.append(seg0)

audio = [
    '      <audio id="a-music" src="assets/audio/music-v3.wav" data-start="0" data-duration="38.4" data-volume="1.0" data-track-index="10"></audio>']
for vo, st in VO_START.items():
    d = r2(T[vo]['duration'] / RATE - 0.005)
    audio.append(f'      <audio id="a-vo-{vo}" src="assets/vo3/{vo}.mp3" data-start="{st}" data-duration="{d}" data-playback-rate="{RATE}" data-track-index="11"></audio>')
sfx = [('a-crt', 'crt-on.wav', 0.0, 0.3, 12), ('a-slam1', 'slam.wav', 0.3, 0.18, 13), ('a-splat1', 'splat.wav', 3.94, 0.25, 12),
       ('a-splat2', 'splat.wav', 5.56, 0.25, 13), ('a-slam2', 'slam.wav', 31.5, 0.18, 13)]
for k, (sid, *_x) in enumerate(SEGS):
    pt = r2(VO_START[_x[4]] + T[_x[4]]['punch'] / RATE)
    sfx.append((f'a-hit{k+1}', 'blip.wav', pt, 0.18, 14 + (k % 2)))
def fdur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, 'assets/audio', f)]).decode())
for aid, f, st, vol, tr in sfx:
    audio.append(f'      <audio id="{aid}" src="assets/audio/{f}" data-start="{st}" data-duration="{r2(fdur(f) - 0.005)}" data-volume="{vol}" data-track-index="{tr}"></audio>')

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

      <!-- roast captions: setup + punchline, timed to the VO's character timestamps -->
{chr(10).join(caps)}
      <div id="cap-end" class="cap clip" data-start="31.5" data-duration="6.9" data-track-index="1"><span class="t">LEMMINGS, BUT THEY'RE <em>VCs.</em></span></div>

      <!-- the computer -->
      <div id="monitor">
        <div id="bezel"></div>
        <div id="tube-frame"></div>
        <div id="screen">
          <!-- cold open: power-on + logo slam -->
          <div id="s0" class="layer clip" data-start="0" data-duration="2.2" data-track-index="2">
            <div id="static"></div>
            <div id="crt-line"></div>
            <div id="logo-stack">
              <img class="ghost warm" src="assets/logo.png" alt="" />
              <img class="ghost cool" src="assets/logo.png" alt="" />
              <img id="logo-base" src="assets/logo.png" alt="VCs" />
            </div>
            <div id="logo-sub"><span id="logo-sub-t">A TRIBUTE TO THE 1991 CLASSIC</span></div>
          </div>
          <!-- one gameplay shot per roast line -->
{chr(10).join(vids)}
          <!-- end screen -->
          <div id="end-screen" class="layer clip" data-start="31.5" data-duration="6.9" data-track-index="2">
            <div id="end-shade"></div>
            <img id="end-logo" src="assets/logo.png" alt="VCs" />
            <div id="press" data-layout-allow-occlusion><span id="press-t" data-layout-allow-occlusion>▶ PRESS START</span></div>
          </div>
          <div id="flash"></div>
          <div id="glass" data-layout-allow-occlusion></div>
        </div>
        <div id="chin">
          <div id="brand"><div id="stripes"><i style="background:#58b848"></i><i style="background:#f0c030"></i><i style="background:#e8742a"></i><i style="background:#d8402a"></i><i style="background:#8a4ab8"></i><i style="background:#3a8ad0"></i></div>VC-1991</div>
          <div id="grille"></div>
          <div id="knobs"><i></i><i></i><span id="led"></span></div>
        </div>
      </div>

      <!-- bottom -->
      <div id="url-line" class="clip" data-start="2.2" data-duration="29.3" data-track-index="4"><span id="url-t">▶ PLAY FREE · <b>lemmingsvc.vercel.app</b></span></div>
      <div id="cta" class="clip" data-start="31.5" data-duration="6.9" data-track-index="4">
        <div id="cta-pill">▶ PLAY FREE <small>lemmingsvc.vercel.app</small></div>
      </div>
      <div id="herd" data-layout-allow-overflow class="clip" data-start="31.5" data-duration="6.9" data-track-index="5">
        <div class="vc" id="vc0"><img src="assets/badge-sequoia.png" alt="" /></div>
        <div class="vc" id="vc1"></div><div class="vc" id="vc2"></div><div class="vc" id="vc3"></div>
        <div class="vc" id="vc4"></div><div class="vc" id="vc5"></div><div class="vc" id="vc6"></div><div class="vc" id="vc7"></div>
      </div>

      <!-- audio: score, VO (ElevenLabs "Adam", eleven_v3, 1.08x), quiet SFX -->
{chr(10).join(audio)}
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      const hash = (n) => {{ const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }};

      // ---- cold open: CRT power-on, then the logo slams with an RGB-split glitch + monitor shake ----
      tl.fromTo("#crt-line", {{ scaleX: 0.02, scaleY: 1, opacity: 1 }}, {{ scaleX: 1, duration: 0.1, ease: "expo.out" }}, 0.02);
      tl.to("#crt-line", {{ scaleY: 150, opacity: 0, duration: 0.18, ease: "power2.in" }}, 0.12);
      tl.fromTo("#static", {{ opacity: 0 }}, {{ opacity: 0.4, duration: 0.06 }}, 0.18);
      tl.to("#static", {{ opacity: 0, duration: 0.2, ease: "power2.out" }}, 0.26);
      tl.fromTo("#logo-stack", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.28, ease: "power4.out" }}, 0.3);
      const ghosts = gsap.utils.toArray("#logo-stack .ghost");
      const amp = {{ a: 0 }};
      tl.set(ghosts, {{ opacity: 0.8 }}, 0.3);
      tl.fromTo(amp, {{ a: 1 }}, {{ a: 0, duration: 0.45, ease: "power3.in", immediateRender: false,
        onUpdate: () => {{ const step = Math.floor(tl.time() / 0.04);
          ghosts.forEach((el, i) => gsap.set(el, {{ x: (hash(step * 13 + i * 7) * 2 - 1) * 26 * amp.a, y: (hash(step * 29 + i * 11) * 2 - 1) * 8 * amp.a }})); }} }}, 0.3);
      tl.set(ghosts, {{ opacity: 0, x: 0, y: 0 }}, 0.76);
      const shake = {{ a: 0 }};
      tl.fromTo(shake, {{ a: 1 }}, {{ a: 0, duration: 0.35, ease: "power2.in", immediateRender: false,
        onUpdate: () => {{ const s = Math.floor(tl.time() / 0.035); gsap.set("#monitor", {{ x: (hash(s) * 2 - 1) * 12 * shake.a, y: (hash(s + 50) * 2 - 1) * 8 * shake.a }}); }} }}, 0.3);
      tl.set("#monitor", {{ x: 0, y: 0 }}, 0.66);
      tl.fromTo("#logo-sub-t", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0.55);

      // ---- roast captions ----
{chr(10).join(tl)}

      // hard-cut flashes
      {json.dumps(CUTS)}.forEach((t) => {{
        tl.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.14, ease: "power2.out", immediateRender: false }}, t);
      }});
      tl.fromTo("#url-t", {{ opacity: 0, y: 12 }}, {{ opacity: 0.9, y: 0, duration: 0.4, ease: "power2.out" }}, 2.4);

      // ---- end card ----
      tl.fromTo("#cap-end .t", {{ scale: 1.8, filter: "blur(16px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.45, ease: "power4.out" }}, 31.5);
      tl.fromTo("#end-logo", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "power4.out" }}, 31.5);
      const shake2 = {{ a: 0 }};
      tl.fromTo(shake2, {{ a: 1 }}, {{ a: 0, duration: 0.3, ease: "power2.in", immediateRender: false,
        onUpdate: () => {{ const s = Math.floor(tl.time() / 0.035); gsap.set("#monitor", {{ x: (hash(s + 9) * 2 - 1) * 10 * shake2.a, y: (hash(s + 70) * 2 - 1) * 6 * shake2.a }}); }} }}, 31.5);
      tl.set("#monitor", {{ x: 0, y: 0 }}, 31.82);
      tl.fromTo("#press-t", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 32.3);
      tl.to("#press-t", {{ opacity: 0.1, duration: 0.01, yoyo: true, repeat: Math.max(0, Math.floor(5.8 / 0.5) - 1), repeatDelay: 0.24 }}, 32.55);
      tl.fromTo("#cta-pill", {{ y: 140, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "circ.out" }}, 31.9);
      tl.to("#cta-pill", {{ scale: 1.04, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.floor(5.8 / 0.8) - 1) }}, 32.5);
      const vcs = gsap.utils.toArray("#herd .vc");
      const herd = {{ p: 0 }};
      tl.fromTo(herd, {{ p: 0 }}, {{ p: 1, duration: 6.8, ease: "none",
        onUpdate: () => {{ const f = Math.floor(tl.time() / 0.07) % 8;
          vcs.forEach((el, i) => {{ const x = -60 + herd.p * 1300 - i * 52 - (i > 3 ? 18 : 0) + 380;
            gsap.set(el, {{ x, backgroundPosition: `${{-((f + i * 3) % 8) * 36}}px 0px` }}); }}); }} }}, 31.55);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w').write(html)
print('built v3')
