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
# v4: groove 0.2-13.2 (roasts) | reveal 13.2-19.2 (drums out, riser, logo hit 14.6) | action 19.2-28.0 (busy) | end hit 28.0-31.0
TOTAL4 = 31.0
m = buf(TOTAL4)
Am, F, C, G = [57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]
prog = [Am, F, C, G]
MEL = [69, 72, 76, 72, 74, 72, 69, 67, 69, 72, 76, 79, 77, 76, 72, 74]


def groove(t_from, t_to, busy, melody_every_other=True):
    t = t_from; step = 0
    while t < t_to - 1e-6:
        ch = prog[int((t - t_from) / (BEAT * 4)) % 4]; bb = step % 4
        add(m, t, tri(mtof(ch[0] - 12), BEAT * 0.48, 0.42))
        add(m, t + BEAT / 2, tri(mtof(ch[0]), BEAT * 0.45, 0.30))
        if bb in (0, 2): add(m, t, kick(0.8))
        if bb in (1, 3): add(m, t, snare())
        for h in range(4 if busy else 2):
            add(m, t + h * BEAT / (4 if busy else 2), hat(0.06 if busy else 0.045))
        if busy or not melody_every_other or (step // 16) % 2 == 1:
            for e in range(2):
                n = MEL[(step * 2 + e) % len(MEL)] + (12 if busy and e == 0 else 0)
                add(m, t + e * BEAT / 2, square(mtof(n), BEAT / 2 * 0.9, 0.08, 0.25, 0.004))
        t += BEAT; step += 1


groove(0.2, 13.2, False)
# reveal: drone + rising arpeggio, soft hit on the logo slam
for i in range(15):
    add(m, 13.2 + i * BEAT, tri(mtof(33), BEAT, 0.3))
arp = [57, 60, 64, 69, 60, 64, 69, 72]
for i, n in enumerate(arp):
    add(m, 13.25 + i * 0.16, square(mtof(n), 0.14, 0.06, 0.5))
add(m, 14.6, kick(0.6))
for n in [45, 57, 64, 69]:
    add(m, 14.6, [x * max(0.0, 1 - i / (4.4 * SR)) for i, x in enumerate(square(mtof(n), 4.4, 0.035, 0.5, 0.003))])
riser = []
for i in range(int(1.4 * SR)):
    tt = i / SR; f = 300 + 1400 * (tt / 1.4) ** 2
    riser.append(math.sin(2 * math.pi * f * tt) * 0.07 * (tt / 1.4))
add(m, 17.8, riser)
groove(19.2, 28.0, True)
add(m, 28.0, kick(0.6))
for n in [45, 57, 60, 64, 69]:
    add(m, 28.0, [x * max(0.0, 1 - i / (3.0 * SR)) for i, x in enumerate(square(mtof(n), 3.0, 0.05, 0.5, 0.003))])
for i, n in enumerate([69, 72, 76, 81]):
    add(m, 28.4 + i * 0.4, square(mtof(n), 0.35, 0.07, 0.25))
write('music-v4.wav', m, 0.9)

# v5: single roast 0.2-5.06 | reveal 5.06-11.04 (logo hit 6.46) | action 11.04-19.88 | end hit 19.85-22.9
m = buf(22.9)
groove(0.2, 5.06, False, melody_every_other=False)
for i in range(15):
    add(m, 5.06 + i * BEAT, tri(mtof(33), BEAT, 0.3))
for i, n in enumerate(arp):
    add(m, 5.1 + i * 0.16, square(mtof(n), 0.14, 0.06, 0.5))
add(m, 6.46, kick(0.6))
for n in [45, 57, 64, 69]:
    add(m, 6.46, [x * max(0.0, 1 - i / (4.4 * SR)) for i, x in enumerate(square(mtof(n), 4.4, 0.035, 0.5, 0.003))])
add(m, 9.64, riser)
groove(11.04, 19.88, True)
add(m, 19.85, kick(0.6))
for n in [45, 57, 60, 64, 69]:
    add(m, 19.85, [x * max(0.0, 1 - i / (3.0 * SR)) for i, x in enumerate(square(mtof(n), 3.0, 0.05, 0.5, 0.003))])
for i, n in enumerate([69, 72, 76, 81]):
    add(m, 20.25 + i * 0.4, square(mtof(n), 0.35, 0.07, 0.25))
write('music-v5.wav', m, 0.9)
