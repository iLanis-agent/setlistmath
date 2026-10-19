// Setlist Math engine: song lengths, gaps and stage slots in whole seconds, exact integer arithmetic.
var TRACK_ERR = "each song length must be minutes and seconds like 3:45 (or hours too, like 1:02:30), above 0:00, separated by commas";
var COUNT_ERR = "enter from 1 to 40 songs";
var GAP_ERR = "the gap between songs must be a whole number of seconds from 0 to 600";
var SLOT_ERR = "the slot must be a whole number of minutes from 1 to 600";

function _tracks(text) {
  text = typeof text === "string" ? text.trim() : "";
  var parts = text === "" ? [] : text.split(",");
  var out = [];
  for (var i = 0; i < parts.length; i++) {
    var p = parts[i].trim(), m = /^([0-9]{1,2}):([0-5][0-9])$/.exec(p), s;
    if (m) s = parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
    else {
      m = /^([0-9]):([0-5][0-9]):([0-5][0-9])$/.exec(p);
      if (!m) throw new Error(TRACK_ERR);
      s = parseInt(m[1], 10) * 3600 + parseInt(m[2], 10) * 60 + parseInt(m[3], 10);
    }
    if (s === 0) throw new Error(TRACK_ERR);
    out.push(s);
  }
  if (out.length < 1 || out.length > 40) throw new Error(COUNT_ERR);
  return out;
}
function _gap(t) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t) || parseInt(t, 10) > 600) throw new Error(GAP_ERR);
  return parseInt(t, 10);
}
function _slot(t) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t) || parseInt(t, 10) < 1 || parseInt(t, 10) > 600) throw new Error(SLOT_ERR);
  return parseInt(t, 10);
}
function _t(s) {
  var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), r = s % 60;
  var rr = (r < 10 ? "0" : "") + r;
  if (h > 0) return h + ":" + (m < 10 ? "0" : "") + m + ":" + rr;
  return m + ":" + rr;
}
function _plural(n, one, many) { return n + " " + (n === 1 ? one : many); }
function _total(tr, gap) { var s = 0; for (var i = 0; i < tr.length; i++) s += tr[i]; return { music: s, stage: s + gap * (tr.length - 1) }; }

function runTruth(tracks, gap) {
  var tr = _tracks(tracks), g = _gap(gap), t = _total(tr, g);
  if (tr.length === 1) return "1 song, " + _t(t.stage) + " on stage.";
  return tr.length + " songs totalling " + _t(t.music) + " plus " + _plural(tr.length - 1, "gap", "gaps") + " of " + _plural(g, "second", "seconds") + ": " + _t(t.stage) + " on stage.";
}
function slotTruth(slot, tracks, gap) {
  var sl = _slot(slot), tr = _tracks(tracks), g = _gap(gap), t = _total(tr, g).stage, cap = sl * 60;
  var head = "Slot of " + _plural(sl, "minute", "minutes") + " (" + _t(cap) + ") and a set of " + _t(t) + " on stage: ";
  if (t > cap) return head + "over by " + _t(t - cap) + ".";
  if (t === cap) return head + "fits exactly.";
  return head + "fits, with " + _t(cap - t) + " spare.";
}
function cutTruth(slot, tracks, gap) {
  var sl = _slot(slot), tr = _tracks(tracks), g = _gap(gap), cap = sl * 60;
  var ends = [], run = 0;
  for (var i = 0; i < tr.length; i++) { run += tr[i] + (i > 0 ? g : 0); ends.push(run); }
  var k = 0;
  while (k < tr.length && ends[k] <= cap) k++;
  var slotText = "in a slot of " + _plural(sl, "minute", "minutes");
  if (k === tr.length) {
    if (k === 1) return "The only song fits " + slotText + ", ending at " + _t(ends[0]) + ".";
    return "All " + k + " songs fit " + slotText + ", ending at " + _t(ends[k - 1]) + ".";
  }
  if (k === 0) return "Not even the first song fits " + slotText + ": it would end at " + _t(ends[0]) + ", " + _t(ends[0] - cap) + " over.";
  var fit = k === 1 ? "The first song fits" : "The first " + k + " songs fit";
  return fit + " " + slotText + ", ending at " + _t(ends[k - 1]) + ". Song " + (k + 1) + " would end at " + _t(ends[k]) + ", " + _t(ends[k] - cap) + " over.";
}
