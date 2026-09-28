"""Generate the v3 'This game is for…' voiceover (ElevenLabs Adam, eleven_v3) with character timestamps.
Writes assets/vo3/<id>.mp3 and assets/vo3/timing.json with each line's duration and punchline onset."""
import base64, json, os, subprocess, urllib.request

KEY = os.environ['ELEVENLABS_API_KEY']  # export your ElevenLabs API key first
VOICE = 'pNInz6obpgDQGcFmaJgB'  # Adam
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'vo3')
LINES = [
    ('l1', '[serious] This game is for contrarian investors... [pause] [deadpan] who ask who else is in.', 'who ask'),
    ('l2', 'For early believers... [pause] who ask if there\'s allocation later.', 'who ask'),
    ('l3', 'For conviction-driven funds... [pause] that just need a lead first.', 'that just'),
    ('l4', 'For thesis-driven firms... [pause] whose thesis is... [deadpan] whatever\'s hot.', 'whose'),
    ('l5', 'For founder-friendly partners... [pause] who\'ll circle back after traction.', 'who\'ll'),
    ('l6', 'For bold, independent thinkers... [pause] [deadpan] who do whatever Sequoia does.', 'who do'),
    ('end', '[dramatic] V.C.s. [pause] Lemmings... but they\'re V.C.s. [upbeat] Play free.', 'Lemmings'),
]
timing = {}
for lid, text, punch in LINES:
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps',
                                 data=json.dumps({'text': text, 'model_id': 'eleven_v3'}).encode(),
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req))
    raw = os.path.join(OUT, lid + '.raw.mp3')
    open(raw, 'wb').write(base64.b64decode(r['audio_base64']))
    al = r.get('alignment') or r.get('normalized_alignment')
    chars = ''.join(al['characters']); starts = al['character_start_times_seconds']; ends = al['character_end_times_seconds']
    # first/last spoken (non-space, non-tag) characters → trim window
    spoken = [i for i, c in enumerate(chars) if c.isalnum()]
    t0, t1 = max(0.0, starts[spoken[0]] - 0.04), ends[spoken[-1]] + 0.12
    k = chars.find(punch)
    punch_t = starts[k] - t0 if k >= 0 else None
    mp3 = os.path.join(OUT, lid + '.mp3')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-to', f'{t1:.3f}', '-i', raw, '-c:a', 'libmp3lame', '-b:a', '192k', mp3], check=True)
    os.remove(raw)
    timing[lid] = {'duration': round(t1 - t0, 3), 'punch': round(punch_t, 3) if punch_t is not None else None}
    print(lid, timing[lid])
json.dump(timing, open(os.path.join(OUT, 'timing.json'), 'w'), indent=1)
