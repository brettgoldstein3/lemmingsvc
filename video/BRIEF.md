---
workflow: general-video
flow: companion
storyboard: no
message: "Lemmings, but they're VCs. The lead goes first; everyone follows. Play free."
destination: x
aspect: "1:1"
length: 23s
language: en
audience: tech/VC Twitter
---

## Intent
~23s square trailer to advertise https://lemmingsvc.vercel.app on X (autoplays muted, so captions carry the story).
Storyboard agreed in chat: CRT power-on + logo slam → "The lead goes first" (Sequoia lead drops from the trapdoor) →
"Everyone follows" (herd walks off the valuation cap: "Right behind you!") → montage (startup curve, burn rate, Series A/B/C, Demo Day) →
"We were early believers" + results screen → end card (logo, tagline, URL, Play free).

## Assets
- Real gameplay captured frame-by-frame from the game (`capture/`, encoded to `assets/clips/*.mp4` at exact 3x).
- Game art from the site: logo, dirt texture, walk sprite, fund badges.

## Customizations
- Audio: original chiptune score + SFX synthesized by `tools/synth.py` (150 BPM grid); game voice clips ("Let's go!", "We're in!");
  ElevenLabs deep trailer VO (voice "Brian"), user chose "chiptune + SFX + trailer VO".
- Aspect: user asked to check X best practices → square 1:1 (uncropped in every feed; vertical risks timeline cropping of captions).

## Notes
- Fonts: Press Start 2P + VT323 (OFL), shipped locally for deterministic render.
