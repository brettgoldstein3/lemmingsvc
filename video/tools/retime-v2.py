"""Retime index.html for the v2 voiceover (ElevenLabs "Adam", eleven_v3): 28.8s, quieter SFX."""
import os, re, subprocess

ROOT = os.path.join(os.path.dirname(__file__), '..')
p = os.path.join(ROOT, 'index.html')
s = open(p).read()


def R(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


def between(start_marker, end_marker, new):
    global s
    i = s.index(start_marker); j = s.index(end_marker)
    s = s[:i] + new + s[j:]


R('data-duration="22.8" data-width="1080"', 'data-duration="28.8" data-width="1080"')

between('      <!-- top captions (one per beat hit) -->', '      <!-- the computer -->', '''      <!-- top captions (one per beat hit) -->
      <div id="cap-lead" class="cap clip" data-start="5.2" data-duration="3.2" data-track-index="1"><span class="t">THE LEAD GOES <em>FIRST.</em></span></div>
      <div id="cap-follow" class="cap clip" data-start="8.4" data-duration="4.0" data-track-index="1"><span class="t">EVERYONE <em>FOLLOWS.</em></span></div>
      <div id="cap-m1" class="cap clip" data-start="12.4" data-duration="1.6" data-track-index="1"><span class="t">OFF THE VALUATION <em>CAP</em></span></div>
      <div id="cap-m2" class="cap clip" data-start="14.0" data-duration="1.6" data-track-index="1"><span class="t">INTO THE BURN <em>RATE</em></span></div>
      <div id="cap-m3" class="cap clip" data-start="15.6" data-duration="1.6" data-track-index="1"><span class="t">THE TROUGH OF <em>SORROW</em></span></div>
      <div id="cap-m4" class="cap clip" data-start="17.2" data-duration="0.6" data-track-index="1"><span class="t">SERIES <em>A, B, C</em></span></div>
      <div id="cap-m5" class="cap clip" data-start="17.8" data-duration="0.6" data-track-index="1"><span class="t">DEMO <em>DAY</em></span></div>
      <div id="cap-every" class="cap quote clip" data-start="18.4" data-duration="2.0" data-track-index="1"><span class="t">EVERY SINGLE ONE OF <em>THEM...</em></span></div>
      <div id="cap-believers" class="cap quote clip" data-start="20.4" data-duration="2.0" data-track-index="1"><span class="t">"WE WERE EARLY <em>BELIEVERS.</em>"</span></div>
      <div id="cap-end" class="cap clip" data-start="22.4" data-duration="6.4" data-track-index="1"><span class="t">LEMMINGS, BUT THEY'RE <em>VCs.</em></span></div>

''')

R('<div id="s1" class="layer clip" data-start="0" data-duration="3.6"', '<div id="s1" class="layer clip" data-start="0" data-duration="5.2"')
between('          <!-- gameplay, cut to the 0.4s beat grid -->', '          <!-- S6: end screen -->', '''          <!-- gameplay, cut to the 0.4s beat grid -->
          <video id="v-lead" src="assets/clips/a-lead.mp4" data-start="5.2" data-duration="3.2" data-track-index="3" muted playsinline></video>
          <video id="v-follow" src="assets/clips/b-follow.mp4" data-start="8.4" data-duration="4.0" data-media-start="0.05" data-track-index="3" muted playsinline></video>
          <video id="v-cap" src="assets/clips/b-follow.mp4" data-start="12.4" data-duration="1.6" data-media-start="1.2" data-track-index="3" muted playsinline></video>
          <video id="v-burn" src="assets/clips/d-burn2.mp4" data-start="14.0" data-duration="1.6" data-media-start="0.2" data-track-index="3" muted playsinline></video>
          <video id="v-curve" src="assets/clips/c-curve2.mp4" data-start="15.6" data-duration="1.6" data-media-start="0.2" data-track-index="3" muted playsinline></video>
          <video id="v-series" src="assets/clips/e-series.mp4" data-start="17.2" data-duration="0.6" data-media-start="0.3" data-track-index="3" muted playsinline></video>
          <video id="v-demoday" src="assets/clips/f-demoday.mp4" data-start="17.8" data-duration="0.6" data-media-start="0.3" data-track-index="3" muted playsinline></video>
          <div id="s5-result" class="layer result-crop clip" data-start="18.4" data-duration="2.0" data-track-index="2"><img src="assets/clips/h-result.png" alt="" /></div>
          <video id="v-exit" src="assets/clips/g-exit.mp4" data-start="20.4" data-duration="2.0" data-media-start="0.2" data-track-index="3" muted playsinline></video>
''')
R('<div id="end-screen" class="layer clip" data-start="18.4" data-duration="4.4"', '<div id="end-screen" class="layer clip" data-start="22.4" data-duration="6.4"')
R('<div id="url-line" class="clip" data-start="3.6" data-duration="14.8"', '<div id="url-line" class="clip" data-start="5.2" data-duration="17.2"')
R('<div id="cta" class="clip" data-start="18.4" data-duration="4.4"', '<div id="cta" class="clip" data-start="22.4" data-duration="6.4"')
R('class="clip" data-start="18.4" data-duration="4.4" data-track-index="5"', 'class="clip" data-start="22.4" data-duration="6.4" data-track-index="5"')

a_start = s.index('      <!-- audio: score, VO, SFX -->')
a_end = s.index('    </div>', a_start)
s = s[:a_start] + '''      <!-- audio: score, VO (ElevenLabs "Adam", eleven_v3), quiet SFX -->
      <audio id="a-music" src="assets/audio/music.wav" data-start="0" data-duration="28.8" data-volume="0.5" data-track-index="10"></audio>
      <audio id="a-vo1" src="assets/vo2/vo1.mp3" data-start="0.3" data-track-index="11"></audio>
      <audio id="a-vo2" src="assets/vo2/vo2.mp3" data-start="5.4" data-track-index="11"></audio>
      <audio id="a-vo3" src="assets/vo2/vo3.mp3" data-start="8.6" data-track-index="11"></audio>
      <audio id="a-vo4" src="assets/vo2/vo4.mp3" data-start="12.5" data-track-index="11"></audio>
      <audio id="a-vo5" src="assets/vo2/vo5.mp3" data-start="18.45" data-track-index="11"></audio>
      <audio id="a-vo6" src="assets/vo2/vo6.mp3" data-start="22.7" data-track-index="11"></audio>
      <audio id="a-crt" src="assets/audio/crt-on.wav" data-start="0" data-volume="0.35" data-track-index="12"></audio>
      <audio id="a-slam1" src="assets/audio/slam.wav" data-start="4.0" data-volume="0.5" data-track-index="13"></audio>
      <audio id="a-door" src="assets/audio/door.wav" data-start="5.8" data-volume="0.3" data-track-index="12"></audio>
      <audio id="a-splat1" src="assets/audio/splat.wav" data-start="10.39" data-volume="0.3" data-track-index="12"></audio>
      <audio id="a-splat2" src="assets/audio/splat.wav" data-start="12.01" data-volume="0.3" data-track-index="13"></audio>
      <audio id="a-splat3" src="assets/audio/splat.wav" data-start="13.24" data-volume="0.3" data-track-index="12"></audio>
      <audio id="a-wh1" src="assets/audio/whoosh.wav" data-start="13.9" data-volume="0.2" data-track-index="13"></audio>
      <audio id="a-wh2" src="assets/audio/whoosh.wav" data-start="15.5" data-volume="0.2" data-track-index="12"></audio>
      <audio id="a-wh3" src="assets/audio/whoosh.wav" data-start="17.1" data-volume="0.2" data-track-index="13"></audio>
      <audio id="a-blip" src="assets/audio/blip.wav" data-start="18.4" data-volume="0.3" data-track-index="12"></audio>
      <audio id="a-slam2" src="assets/audio/slam.wav" data-start="22.4" data-volume="0.5" data-track-index="13"></audio>
''' + s[a_end:]

# ---- timeline ----
R('tl.fromTo(tw, { n: 0 }, { n: TW.length, duration: 1.9, ease: "none",', 'tl.fromTo(tw, { n: 0 }, { n: TW.length, duration: 2.9, ease: "none",')
R('tl.to("#tw-wrap", { opacity: 0, duration: 0.12 }, 2.82);', 'tl.to("#tw-wrap", { opacity: 0, duration: 0.12 }, 3.85);')
R('{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }, 2.9);', '{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }, 4.0);')
R('tl.set(ghosts, { opacity: 0.8 }, 2.9);', 'tl.set(ghosts, { opacity: 0.8 }, 4.0);')
R('* 8 * amp.a })); } }, 2.9);', '* 8 * amp.a })); } }, 4.0);')
R('tl.set(ghosts, { opacity: 0, x: 0, y: 0 }, 3.36);', 'tl.set(ghosts, { opacity: 0, x: 0, y: 0 }, 4.46);')
R('* 8 * shake.a }); } }, 2.9);', '* 8 * shake.a }); } }, 4.0);')
R('tl.set("#monitor", { x: 0, y: 0 }, 3.26);', 'tl.set("#monitor", { x: 0, y: 0 }, 4.36);')
R('{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 3.1);', '{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 4.2);')
between('      // ---- captions: kinetic beat slam, distinct entrances ----', '      // URL line: fades in once gameplay starts', '''      // ---- captions: kinetic beat slam, distinct entrances ----
      tl.fromTo("#cap-lead .t", { scale: 1.6, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.45, ease: "power4.out" }, 5.2 + BEAT * 0.5);
      tl.fromTo("#cap-follow .t", { y: 90, rotation: 5, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "circ.out" }, 8.4 + BEAT * 0.5);
      [["#cap-m1", 12.4], ["#cap-m2", 14.0], ["#cap-m3", 15.6], ["#cap-m4", 17.2], ["#cap-m5", 17.8]].forEach(([id, t], i) => {
        const dir = i % 2 ? 1 : -1;
        tl.fromTo(id + " .t", { x: dir * 420, opacity: 0 }, { x: 0, opacity: 1, duration: 0.28, ease: "expo.out" }, t);
      });
      tl.fromTo("#cap-every .t", { y: -70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 18.4 + BEAT * 0.5);
      tl.fromTo("#cap-believers .t", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" }, 20.4 + BEAT * 0.5);
      tl.fromTo("#cap-end .t", { scale: 1.8, filter: "blur(16px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.45, ease: "power4.out" }, 22.4);

      // hard-cut flashes, on the beat grid
      [5.2, 8.4, 12.4, 14.0, 15.6, 17.2, 17.8, 18.4, 20.4, 22.4].forEach((t) => {
        tl.fromTo("#flash", { opacity: 0.5 }, { opacity: 0, duration: 0.14, ease: "power2.out", immediateRender: false }, t);
      });

''')
R('{ opacity: 0.9, y: 0, duration: 0.4, ease: "power2.out" }, 3.9);', '{ opacity: 0.9, y: 0, duration: 0.4, ease: "power2.out" }, 5.5);')
R('{ scale: 1, opacity: 1, duration: 0.35, ease: "power4.out" }, 18.4);', '{ scale: 1, opacity: 1, duration: 0.35, ease: "power4.out" }, 22.4);')
R('* 6 * shake2.a }); } }, 18.4);', '* 6 * shake2.a }); } }, 22.4);')
R('tl.set("#monitor", { x: 0, y: 0 }, 18.72);', 'tl.set("#monitor", { x: 0, y: 0 }, 22.72);')
R('{ opacity: 1, duration: 0.01 }, 19.2);', '{ opacity: 1, duration: 0.01 }, 23.2);')
R('Math.floor(3.4 / 0.5) - 1), repeatDelay: 0.24 }, 19.45);', 'Math.floor(5.2 / 0.5) - 1), repeatDelay: 0.24 }, 23.45);')
R('{ y: 0, opacity: 1, duration: 0.5, ease: "circ.out" }, 18.8);', '{ y: 0, opacity: 1, duration: 0.5, ease: "circ.out" }, 22.8);')
R('Math.floor(3.4 / 0.8) - 1) }, 19.4);', 'Math.floor(5.2 / 0.8) - 1) }, 23.4);')
R('{ p: 1, duration: 4.3, ease: "none",', '{ p: 1, duration: 6.3, ease: "none",')
R('}); } }, 18.45);', '}); } }, 22.45);')


# every <audio> gets its real duration (keeps the lint's overlap check honest)
def dur(f):
    return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(ROOT, f)]).decode().strip())


def fix(m):
    tag = m.group(0)
    if 'data-duration' in tag:
        return tag
    src = re.search(r'src="([^"]+)"', tag).group(1)
    return tag.replace(' data-start=', f' data-duration="{round(dur(src) - 0.005, 3)}" data-start=', 1)


s = re.sub(r'<audio [^>]*></audio>', fix, s)
open(p, 'w').write(s)
print('retimed')
