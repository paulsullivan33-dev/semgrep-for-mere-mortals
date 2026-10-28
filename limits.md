# Limits

What Semgrep cannot do, and what it must
not be asked to do — the chapter the rest
of the guide has been promising.

## Patterns see shapes, not meaning

A pattern knows that `eval(` is a call.
It does not know — cannot know — whether
the argument is a constant the author
controls or text mailed in by a stranger.
The open-source engine's matching is
grammatical, not moral: it reports the
shape and leaves the meaning to you.
Every consequence in this chapter grows
from that one fact. A finding is a claim
to check (chapter 8), a clean scan is an
absence of *matches*, and neither is a
verdict about safety. Tools that claim
more are claiming the part a human does.

## The eye is local

By default the engine matches within a
file, and its view of a single statement
is exact while its view of a program is
sketchy. Taint mode (chapter 10) follows
values further — through a file's
assignments and calls — but the
open-source engine does not trace data
across file boundaries, and a journey
that hops through a database, a queue, a
config file or another program leaves its
sight entirely. Cross-file dataflow and
reachability judgements are the
commercial platform's territory (chapters
2 and 12), documented-only in this guide.
A flaw whose halves live in different
files is invisible here — not unlikely to
be found, but outside the instrument.

## A rule finds only what it looks for

The guide's own evidence, assembled:

- The lab's six rules missed three of
  the six flaws planted in a forty-line
  file — the two glued queries and the
  MD5 hash — because no rule looked for
  them (chapter 4).
- The registry's 151-rule Python pack
  missed the `eval()`, the plaintext
  password and both glued queries in the
  same file (chapter 6).
- A `curl … | bash` line survived every
  scan in the book, lab rules and
  professional packs alike, because no
  engaged rule spoke to it (chapter 9).

None of these scanners malfunctioned.
Each looked for exactly what it was told
to look for. **The set of rules you run
is the set of flaws you can find,** and
the complement — everything else — is
not certified clean; it is merely
unexamined. The practical meaning: choose
packs for your stack, write rules for
your own history of mistakes, and never
let a green scan end a conversation that
a threat model should finish.

## Silence is ambiguous

Chapter 5's trap deserves its place here:
a rule that lists several languages can
match in one and stay silent in another,
and a pattern that is subtly wrong
matches nothing at all. Semgrep cannot
distinguish *no flaws* from *no working
rules* — both print `0 findings`. The
defences are chapter 10's tests (a rule
proven to fire on code written to trigger
it), chapter 4's habit of scanning a
known-flawed fixture before trusting a
ruleset on real code, and a reader's
reflex: when a scan of real code is
surprisingly clean, suspect the rules
before you celebrate the code.

## Findings cost attention, and can be wrong

Rules guess. The lab's own password rule
keys on a variable's *name*: it would
fire on `password = "ask the user"` in a
form-handling example, and stay silent
for a real secret stored in a variable
named `x`. Registry rules carry the same
nature at scale — which is why chapter 8
treats triage as normal operation, and
why a team that enables every pack at
once usually disables scanning entirely
within a month. A scanner that cries wolf
at volume trains its humans to ignore it,
and an ignored scanner is worse than none:
it provides the *feeling* of a check.
Curate. A short list of rules you believe,
kept green, beats the registry entire.

## The snapshot problem, and performance

A scan is a photograph: true of the code
at that moment, silent about the next
commit. That is why chapter 11 wires the
scan into the act of committing rather
than running it as an occasional audit.
And while the lab's scans finished in
seconds, very large trees make any
per-file engine work for its living;
folder scoping, `.semgrepignore`, and (on
the platform side, documented-only) scan
splitting are the levers. Nothing in this
guide's lab strained the engine, and the
guide does not pretend otherwise.

## The ethical edge

Chapter 1's rule — *your code, your
machines, or explicit permission* — has a
scanner-specific sharpness. A rule pack
is a list of known weaknesses; run over
code you have no right to inspect, the
*output* is a map of someone else's
vulnerabilities, and producing that map
is the act the rule forbids, whether or
not you ever use it. Three corollaries:

- **Open source is published to be read**
  — scanning it on your own machine, to
  decide your own trust, is reading.
  Publishing a "wall of shame" of a small
  project's findings, unreported and
  uninvited, is not the same act, and
  this guide wants no part of it. Found
  something real in someone else's
  project? Tell the maintainers, privately,
  the way you would want to be told.
- **Rules are content from strangers.**
  A rule file is patterns, not programs —
  it cannot run code on your machine —
  but a *config* can point at URLs, and
  borrowed YAML deserves the same glance
  as borrowed anything. The official
  registry is the curated source; prefer
  it, and keep local copies of what your
  projects depend on.
- **Your own findings are sensitive.**
  A scan report of your employer's or
  your own codebase is a list of its
  weaknesses: store it like one. (Semgrep
  itself redacts secret-looking matches in
  its output, chapter 4 — follow its
  example when you paste results anywhere.)
