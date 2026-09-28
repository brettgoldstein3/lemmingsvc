"""v4 voiceover: 3 roast lines → reveal → action lines → CTA. ElevenLabs Adam (eleven_v3) with character timestamps.
Writes assets/vo4/<id>.mp3 and assets/vo4/timing.json: duration + onset (s, from trimmed start) of each marker phrase."""
import base64, json, os, subprocess, urllib.request

KEY = os.environ['ELEVENLABS_API_KEY']  # export your ElevenLabs API key first
VOICE = 'pNInz6obpgDQGcFmaJgB'  # Adam
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'vo4')
LINES = [
    ('r1', '[serious] This game is for contrarian investors... [deadpan] who ask who else is in.', ['who ask']),
    ('r2', 'For early believers... who ask if there\'s allocation later.', ['who ask']),
    ('r3', 'And for bold, independent thinkers... [deadpan] who do whatever Sequoia does.', ['who do']),
    ('intro', '[dramatic] Introducing... V.C.s. An adaptation of the 1990s classic, Lemmings.', ['V.C.s', 'An adaptation']),
    ('a1', '[energetic] Lead the herd through the data room, the burn rate, and Demo Day.', ['the data room', 'the burn rate', 'Demo Day']),
    ('a2', '[energetic] Dig. Build. Bash. Block. Get every V.C. into the round.', ['Dig', 'Build', 'Bash', 'Block', 'Get every']),
    ('cta', '[upbeat] Play it for free.', ['Play']),
]
timing = {}
for lid, text, markers in LINES:
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps',
                                 data=json.dumps({'text': text, 'model_id': 'eleven_v3'}).encode(),
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req))
    raw = os.path.join(OUT, lid + '.raw.mp3')
    open(raw, 'wb').write(base64.b64decode(r['audio_base64']))
    al = r.get('alignment') or r.get('normalized_alignment')
    chars = ''.join(al['characters']); starts = al['character_start_times_seconds']; ends = al['character_end_times_seconds']
    spoken = [i for i, c in enumerate(chars) if c.isalnum()]
    t0, t1 = max(0.0, starts[spoken[0]] - 0.03), ends[spoken[-1]] + 0.1
    marks = {}
    pos = 0
    for mk in markers:
        k = chars.find(mk, pos)
        if k >= 0:
            marks[mk] = round(starts[k] - t0, 3); pos = k + 1
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', raw, '-c:a', 'libmp3lame', '-b:a', '192k', os.path.join(OUT, lid + '.mp3')], check=True)
    os.remove(raw)
    timing[lid] = {'duration': round(t1 - t0, 3), 'marks': marks}
    print(lid, timing[lid])
json.dump(timing, open(os.path.join(OUT, 'timing.json'), 'w'), indent=1)
