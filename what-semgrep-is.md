# What Semgrep Is

Every program is full of shapes: a function
called with a dangerous argument, a query
built by gluing text together, a password
sitting in the source where anyone can read
it. You learn to spot these shapes by eye,
one file at a time, and your eye gets tired
long before the codebase does.

**Semgrep is a scanner that looks for shapes
in code.** You describe the shape you care
about — a **pattern**, written in code that
looks like the code you are hunting — and
Semgrep reads every file you point it at,
parses each one into its grammatical
structure (its **syntax tree**), and reports
every place the shape occurs. Each report is
a **finding**: the rule that matched, the
file, the line, and the message you or the
rule's author wrote for exactly this moment.

The name is a fair description: *semantic
grep*. The old `grep` tool finds letters —
the characters e-v-a-l wherever they appear,
in code, in comments, in strings. Semgrep
finds the *call*: `eval(...)` used as a call,
with any spacing, any argument, in any
function, while ignoring the word "eval"
sitting harmlessly in a comment. That one
step — from letters to grammar — is the
whole idea, and the rest of this guide is
detail.

## Why anyone would do this

- **Code review that scales.** A reviewer
  can check a change for the three mistakes
  she cares about. She cannot check ten
  thousand lines for them, every week,
  without missing one. A rule can, and it
  never gets bored.
- **Learning what "bad" looks like.** A
  finding comes with the rule's message:
  why this shape is dangerous and what to
  do instead. Scanning a project of your
  own is a guided tour of your own habits.
- **House rules, enforced kindly.** Every
  team has a "we don't do it that way here"
  list. Written as Semgrep rules, the list
  checks itself and explains itself at the
  moment it matters — while the code is
  being written, not after it ships.
- **Checking up.** Code you depend on —
  your own old projects, a library you are
  about to adopt — can be asked fair
  questions: does it ever call `eval`? does
  it build SQL by gluing strings? Your code
  or code you may inspect: a fair question,
  and a scanner answers it in seconds.

## The rule, stated before everything else

A tool that reads code looking for weaknesses
can be pointed at anyone's code, and a list
of a program's weaknesses is valuable to
people other than its owner. So this guide
has one rule, and it is not fine print:

> **Scan only code that is yours — on
> machines you own, or where the code's
> owner has given you explicit permission.**

Reviewing your own projects: yes. Running
the public rules over an open-source library
on your own machine, to decide whether to
trust it: that is reading code that was
published to be read, on your machine, for
your decision. Taking a scanner to an
employer's proprietary codebase you were
never asked to audit, a leaked source tree,
or a competitor's product: no. The line is
the same one this series draws for every
inspection tool, and chapter 13 returns to
it. The lab in this guide stayed well inside
it: every line scanned was written for the
lab, flaws and all.

## A first taste

After installing (chapter 3), the whole
tool is one command. This is the lab's
first scan, from chapter 4:

```bash
semgrep scan --config rules/lab-rules.yaml fixtures/shop.py
```

`--config` names the rules — here a small
file the lab wrote itself; chapter 6 uses
packs of rules from the public registry
instead. The last word names what to scan:
one file, or a folder, or a whole project.
The scan of the lab's deliberately flawed
practice file answers (transcript
`semgrep-lab/transcripts/t01-first-scan.txt`):

```text
Ran 3 rules on 1 file: 3 findings.
```

Three of the flaws the lab planted, found
and explained. Two more planted flaws in
the same file were *not* found — by the
lab's rules or by two famous registry packs
— and chapter 13 is honest about why.
A scanner finds what someone taught it to
look for. Teaching it is chapters 5 and 6.

## Who it is for

The programmer who reviews code — their
own or their team's — and wants the
mechanical checks done mechanically. The
maintainer of a growing project whose
"we don't do that here" list lives in
their head and deserves to live in a file.
The curious owner of a folder full of old
scripts, wondering what habits are hiding
in them. The common thread is one person,
their own code, and questions that the
code itself can answer.

## What it is not

Semgrep is not a proof of safety: a clean
scan means no rule matched, and chapter 13
lists the ways real flaws hide from
patterns. It is not a test suite: it never
runs your program, so it cannot tell you
the program works. It is not an exploit
tool: it reports shapes in code you hand
it, and using findings about code you have
no right to inspect crosses the rule above.
And it is not a replacement for reading:
every finding is a claim to check, not a
verdict — chapter 8 is about the checking.
