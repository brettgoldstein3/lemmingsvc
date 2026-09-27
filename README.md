# VCs

**Play: https://lemmingsvc.vercel.app**

Lemmings, but they're VCs. Guide the herd into your round before they follow each other off a cliff.

A single-file browser game: a tribute to the 1991 classic with 9 startup-themed levels (the data room, the startup curve, burn rate, Series A/B/C, Demo Day…).

## Play locally

```bash
python3 -m http.server 8742
```

Then open http://localhost:8742.

## Controls

- Click a skill, then click a VC (keys 1–8 or F3–F10 pick skills)
- F1 / F2: release rate · P: pause · F: fast forward · double-click the mushroom (or F12): nuke
- S: sound on/off · M: music on/off (both start off)
- Touch: drag to scroll, tap a VC to assign

## Deploy

```bash
./deploy.sh
```

## Tests

Every level has an automated "idle loses" and "solution wins" check. In the browser console:

```js
await import('./tests.js').then(m => m.run())
```

## Credits

Game mechanics ported from [Lemmings.ts](https://github.com/tomsoftware/Lemmings.ts) (MIT, Thomas Zeugner). All art, levels and music are original. Voice clips generated with ElevenLabs. Not affiliated with any of the funds whose marks appear in the game.
