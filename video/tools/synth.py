"""Original chiptune score + SFX for the VCs trailer. Pure Python, writes 44.1kHz mono WAVs.

Beat grid: 150 BPM (0.4 s/beat). Scene boundaries land on beats:
  intro 0-5.2 (logo slam 4.0) | groove 5.2-12.4 | montage 12.4-18.4 | payoff 18.4-22.4 | end card 22.4-28.8
Noise elements (snare, hats, crashes, static) are deliberately quiet: they read as harsh on phone speakers.
"""
import math, random, struct, wave, os

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
os.makedirs(OUT, exist_ok=True)
BEAT = 0.4
TOTAL = 38.4
rnd = random.Random(7)


def buf(sec):
    return [0.0] * int(sec * SR)


def write(name, b, gain=1.0):
    peak = max(1e-9, max(abs(x) for x in b))
    k = gain * 0.89 / peak
    with wave.open(os.path.join(OUT, name), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x * k)) * 32767)) for x in b))


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def add(b, t0, sig):
    i0 = int(t0 * SR)
    for i, v in enumerate(sig):
        j = i0 + i
        if 0 <= j < len(b):
            b[j] += v


def env(n, a=0.004, r=0.05, sus=1.0, dur=None):
    out = []
    A, R = int(a * SR), int(r * SR)
    for i in range(n):
        e = min(1.0, i / max(1, A)) * sus
        if i > n - R:
            e *= max(0.0, (n - i) / max(1, R))
        out.append(e)
    return out


def square(freq, sec, vol=0.2, duty=0.25, vib=0.0):
    n = int(sec * SR); e = env(n, 0.003, min(0.06, sec * 0.4)); out = []; ph = 0.0
    for i in range(n):
        f = freq * (1 + vib * math.sin(2 * math.pi * 5.5 * i / SR))
        ph = (ph + f / SR) % 1.0
        out.append((1.0 if ph < duty else -1.0) * vol * e[i])
    return out


def tri(freq, sec, vol=0.3):
    n = int(sec * SR); e = env(n, 0.004, min(0.05, sec * 0.3)); out = []; ph = 0.0
    for i in range(n):
        ph = (ph + freq / SR) % 1.0
        out.append((4 * abs(ph - 0.5) - 1) * vol * e[i])
    return out


def kick(vol=0.9):
    n = int(0.16 * SR); out = []; ph = 0.0
    for i in range(n):
        t = i / SR; f = 45 + 120 * math.exp(-t * 30)
        ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * vol * math.exp(-t * 18))
    return out


def noise(sec, vol, decay, hp=0.0):
    n = int(sec * SR); out = []; prev = 0.0
    for i in range(n):
        x = rnd.uniform(-1, 1)
        y = x - hp * prev; prev = x  # crude high-pass
        out.append(y * vol * math.exp(-i / SR * decay))
    return out


def snare():
    return [a + b for a, b in zip(noise(0.12, 0.16, 26, 0.6), tri(190, 0.14, 0.3))]


def hat(vol=0.05):
    return noise(0.03, vol, 110, 0.95)


# ---------------- music ----------------
# v3 "This game is for…" cut: cold-open slam 0.3 | groove 2.2-31.5 (busier from 21.0) | riser 29.9 | end card 31.5-38.4
m = buf(TOTAL)
Am, F, C, G = [57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]
add(m, 0.3, kick(0.5))
for n in [45, 57, 64]:
    add(m, 0.3, [x * max(0.0, 1 - i / (1.9 * SR)) for i, x in enumerate(square(mtof(n), 1.9, 0.03, 0.5))])
for i, n in enumerate([57, 60, 64, 69, 72, 76, 81, 84]):
    add(m, 1.0 + i * 0.15, square(mtof(n), 0.13, 0.045, 0.5))
prog = [Am, F, C, G]
MEL = [69, 72, 76, 72, 74, 72, 69, 67, 69, 72, 76, 79, 77, 76, 72, 74]
t = 2.2; step = 0
while t < 31.5 - 1e-6:
    bar = int((t - 2.2) / (BEAT * 4)) % 4
    ch = prog[bar]; beat_in_bar = step % 4; busy = t >= 21.0
    add(m, t, tri(mtof(ch[0] - 12), BEAT * 0.48, 0.42))
    add(m, t + BEAT / 2, tri(mtof(ch[0]), BEAT * 0.45, 0.30))
    if beat_in_bar in (0, 2):
        add(m, t, kick(0.8))
    if beat_in_bar in (1, 3):
        add(m, t, snare())
    for h in range(4 if busy else 2):
        add(m, t + h * BEAT / (4 if busy else 2), hat(0.06 if busy else 0.045))
    if (step // 16) % 2 == 1 or busy:  # melody sits out every other phrase so the VO breathes
        for e in range(2):
            n = MEL[(step * 2 + e) % len(MEL)] + (12 if busy and e == 0 else 0)
            add(m, t + e * BEAT / 2, square(mtof(n), BEAT / 2 * 0.9, 0.08, 0.25, 0.004))
    t += BEAT; step += 1
riser = []
for i in range(int(1.6 * SR)):
    tt = i / SR; f = 300 + 1400 * (tt / 1.6) ** 2
    riser.append(math.sin(2 * math.pi * f * tt) * 0.08 * (tt / 1.6))
add(m, 29.9, riser)
add(m, 31.5, kick(0.6))
for n in [45, 57, 60, 64, 69]:
    add(m, 31.5, [x * max(0.0, 1 - i / (6.8 * SR)) for i, x in enumerate(square(mtof(n), 6.8, 0.06, 0.5, 0.003))])
for i, n in enumerate([69, 72, 76, 81, 76, 81, 84, 88]):
    add(m, 31.9 + i * 0.4, square(mtof(n), 0.35, 0.08, 0.25))
write('music-v3.wav', m, 0.9)

# ---------------- SFX ----------------
crt = buf(0.9)
add(crt, 0, noise(0.04, 0.3, 50))                                   # power click
hum = [math.sin(2 * math.pi * (60 + 900 * (i / SR) ** 2) * i / SR) * 0.25 * min(1, i / 2000) * max(0, 1 - i / (0.85 * SR)) for i in range(int(0.85 * SR))]
add(crt, 0.02, hum); add(crt, 0.05, noise(0.4, 0.04, 9, 0.9))       # rising whine + a hint of static
write('crt-on.wav', crt, 0.8)

sl = buf(1.0); add(sl, 0, kick(1.0)); add(sl, 0, noise(0.6, 0.08, 7)); write('slam.wav', sl, 0.95)

wh = buf(0.45)
add(wh, 0, [math.sin(2 * math.pi * (200 + 900 * i / (0.45 * SR)) * i / SR) * 0.4 * math.sin(math.pi * i / (0.45 * SR)) ** 2 for i in range(int(0.45 * SR))])  # tonal swoosh, no hiss
write('whoosh.wav', wh, 0.6)

door = buf(0.5); add(door, 0, noise(0.3, 0.6, 12)); add(door, 0, tri(110, 0.28, 0.4)); write('door.wav', door, 0.8)
spl = buf(0.3); add(spl, 0, noise(0.22, 0.8, 20)); add(spl, 0, tri(90, 0.12, 0.5)); write('splat.wav', spl, 0.8)
blip = buf(0.2); add(blip, 0, square(mtof(88), 0.06, 0.3, 0.5)); add(blip, 0.06, square(mtof(93), 0.08, 0.3, 0.5)); write('blip.wav', blip, 0.6)
print('ok')
