# Setlist Math

Set timing arithmetic. Six songs of 3:45 to 5:20 with 20 second gaps run 25:28 on stage, so a 20 minute slot only fits the first 4 songs.

## What it computes

Song lengths are minutes and seconds (or hours too, like 1:02:30), separated by commas, up to 40 songs. Gaps are whole seconds from 0 to 600. Slots are whole minutes from 1 to 600.

- **The run truth** - total music, the gaps between songs and the total time on stage.
- **The slot truth** - the whole set against a slot: over by how much, fits exactly, or the time to spare.
- **The cut truth** - playing in order, how many songs finish inside the slot, when they end, and by how much the next song overruns.

## Boundary

Arithmetic only. It adds up the song lengths, gaps and slot the owner types. It does not know the songs, the stage changeovers, an organizer's rules or what an audience will sit through, and gives no verdict on whether any set is good, safe or allowed.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (whole seconds, exact integers).
- `oracle.py` - the Python mirror (walks the show on a clock, song by song) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (147 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/setlistmath/
Repo: https://github.com/iLanis-agent/setlistmath
