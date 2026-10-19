#!/usr/bin/env python3
# Setlist Math oracle - mirrors engine.js by walking the show on a clock, song by song, instead of summing.
import json, re, random

TRACK_ERR = "each song length must be minutes and seconds like 3:45 (or hours too, like 1:02:30), above 0:00, separated by commas"
COUNT_ERR = "enter from 1 to 40 songs"
GAP_ERR = "the gap between songs must be a whole number of seconds from 0 to 600"
SLOT_ERR = "the slot must be a whole number of minutes from 1 to 600"

def tracks(text):
    text = text.strip() if isinstance(text, str) else ""
    parts = [] if text == "" else text.split(",")
    out = []
    for p in parts:
        p = p.strip()
        m = re.fullmatch(r"([0-9]{1,2}):([0-5][0-9])", p)
        if m: s = int(m.group(1)) * 60 + int(m.group(2))
        else:
            m = re.fullmatch(r"([0-9]):([0-5][0-9]):([0-5][0-9])", p)
            if not m: raise ValueError(TRACK_ERR)
            s = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        if s == 0: raise ValueError(TRACK_ERR)
        out.append(s)
    if not 1 <= len(out) <= 40: raise ValueError(COUNT_ERR)
    return out
def gapv(t):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or int(t) > 600: raise ValueError(GAP_ERR)
    return int(t)
def slotv(t):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not 1 <= int(t) <= 600: raise ValueError(SLOT_ERR)
    return int(t)
def tm(s):
    h, rest = divmod(s, 3600); m, r = divmod(rest, 60)
    return (f"{h}:{m:02d}:{r:02d}" if h else f"{m}:{r:02d}")
def pl(n, a, b): return f"{n} {a if n == 1 else b}"
def timeline(tr, g):
    clock = 0; ends = []; music = 0
    for i, s in enumerate(tr):
        if i: clock += g
        clock += s; music += s; ends.append(clock)
    return ends, music

def run(t, g):
    tr = tracks(t); g = gapv(g); ends, music = timeline(tr, g)
    if len(tr) == 1: return f"1 song, {tm(ends[-1])} on stage."
    return f"{len(tr)} songs totalling {tm(music)} plus {pl(len(tr)-1,'gap','gaps')} of {pl(g,'second','seconds')}: {tm(ends[-1])} on stage."
def slot(sl, t, g):
    sl = slotv(sl); tr = tracks(t); g = gapv(g); ends, _ = timeline(tr, g); cap = sl * 60; tot = ends[-1]
    head = f"Slot of {pl(sl,'minute','minutes')} ({tm(cap)}) and a set of {tm(tot)} on stage: "
    if tot > cap: return head + f"over by {tm(tot-cap)}."
    if tot == cap: return head + "fits exactly."
    return head + f"fits, with {tm(cap-tot)} spare."
def cut(sl, t, g):
    sl = slotv(sl); tr = tracks(t); g = gapv(g); ends, _ = timeline(tr, g); cap = sl * 60
    k = sum(1 for e in ends if e <= cap) if all(ends[i] < ends[i+1] for i in range(len(ends)-1)) else None
    st = f"in a slot of {pl(sl,'minute','minutes')}"
    if k == len(tr):
        if k == 1: return f"The only song fits {st}, ending at {tm(ends[0])}."
        return f"All {k} songs fit {st}, ending at {tm(ends[-1])}."
    if k == 0: return f"Not even the first song fits {st}: it would end at {tm(ends[0])}, {tm(ends[0]-cap)} over."
    fit = "The first song fits" if k == 1 else f"The first {k} songs fit"
    return f"{fit} {st}, ending at {tm(ends[k-1])}. Song {k+1} would end at {tm(ends[k])}, {tm(ends[k]-cap)} over."

FNS = {"runTruth": lambda a: run(a[0], a[1]), "slotTruth": lambda a: slot(*a), "cutTruth": lambda a: cut(*a)}
T = "3:45, 4:10, 2:58, 5:20, 3:30, 4:05"

def mk(rnd):
    n = rnd.randint(1, 12)
    return ", ".join(f"{rnd.randint(0,12)}:{rnd.randint(0,59):02d}" if rnd.random() < .97 else "1:00:00" for _ in range(n)).replace("0:00", "0:07")

def cases():
    c = []; rnd = random.Random(697)
    for a in [[T,"20"],[T,"0"],["3:45","20"],["3:45","0"],["1:02:30","0"],["0:01","600"],["0:01, 0:01","1"],["99:59, 99:59","600"],[" 3:45 , 4:10 ","5"],["3:45,4:10","5"],
              ["","20"],[",","20"],["3:45,","20"],["0:00","20"],["3:60","20"],["3:5","20"],["345","20"],["3:45","601"],["3:45","-1"],["3:45",""],["3:45","2.5"],["1:00:00","0"],["10:00:00","0"],["1:2:03","0"],["3:45, x","5"]]:
        c.append(("runTruth", a))
    c.append(("runTruth", [", ".join(["0:30"]*40), "10"])); c.append(("runTruth", [", ".join(["0:30"]*41), "10"]))
    for _ in range(25): c.append(("runTruth", [mk(rnd), str(rnd.randint(0,90))]))
    for a in [["30",T,"20"],["25",T,"20"],["26",T,"20"],["1",T,"20"],["600",T,"20"],["1","1:00","0"],["1","1:01","0"],["1","0:59","0"],["0",T,"20"],["601",T,"20"],["x",T,"20"],["",T,"20"],["30","","20"],["30",T,"x"],[" 30 ",T," 20 "],["2","1:00, 0:59","1"],["2","1:00, 1:00","0"],["2","1:00, 1:00","1"]]:
        c.append(("slotTruth", a))
    for _ in range(25): c.append(("slotTruth", [str(rnd.randint(1,60)), mk(rnd), str(rnd.randint(0,60))]))
    for a in [["20",T,"20"],["45",T,"20"],["3",T,"20"],["10","3:45","0"],["4","3:45","0"],["3","3:45","0"],["21",T,"20"],["17",T,"20"],["18",T,"20"],["1","1:00","0"],["2","1:00, 1:00","0"],["2","1:00, 1:00","1"],["1","0:59, 0:01","0"],["1","0:30, 0:30","0"],["1","0:30, 0:30","1"],
              ["0",T,"20"],["x",T,"20"],["20","","20"],["20",T,"601"],["600","1:00:00","0"],["1","1:00:00","0"],[" 20 ",T," 20 "]]:
        c.append(("cutTruth", a))
    for _ in range(30): c.append(("cutTruth", [str(rnd.randint(1,40)), mk(rnd), str(rnd.randint(0,60))]))
    return c

out = []
for fn, args in cases():
    try: exp = FNS[fn](args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1); f.write("\n")
print(len(out), "cases written")
