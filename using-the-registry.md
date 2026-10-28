# Using the Registry

Outcome of this chapter: you borrow other
people's rule-writing at scale — two real
packs from the public registry, run over
the lab's own fixtures — and you can say
exactly what the borrowed rules found,
what they missed, and what that teaches
about packs.

## A pack is a config with a short name

Chapter 2's last config shape needs no
file of yours at all:

```bash
semgrep scan --config p/python --metrics=off fixtures/shop.py fixtures/clean.py
```

`p/python` is a **pack**: a curated bundle
in the public registry at semgrep.dev, in
this case "the Python pack". Semgrep
downloads the pack's rules at scan time —
so this needs the network, and it worked
in the lab logged out, no account — and
runs them like any other config. The full
output is transcript
`semgrep-lab/transcripts/t04-registry-python.txt`:

```text
Ran 151 rules on 2 files: 3 findings.
```

One hundred and fifty-one rules, written
by people who scan Python for a living,
against the lab's two little files. The
three findings, all in `shop.py`:

- `python.lang.security.audit.subprocess-shell-true.subprocess-shell-true`,
  line 32 — the shell call, found by a
  stranger's rule saying the same thing as
  the lab's own, with a longer explanation
  and a **Details link** (`https://sg.run/…`)
  to the rule's page in the registry.
- Two rules on line 37, the MD5 hash:
  `insecure-hash-algorithm-md5` (MD5 is
  not collision-resistant) and
  `md5-used-as-password` (MD5 is too fast
  to hash passwords) — the pack sees the
  same line two ways, because two authors
  cared about it for different reasons.
  Neither is wrong; expect overlaps like
  this whenever a pack is a crowd.

Registry findings also show an `Autofix`
line — here `Autofix ▶ False`, meaning
this rule offers no automatic rewrite
(chapter 11 shows one that does).

## What 151 rules missed

The same file, remember, contains a
password in plain text (line 13), two SQL
queries glued together from caller text
(lines 18–19 and 26), and an `eval()`
(line 42). The Python pack reported none
of them. Not because the pack is bad — it
is a good pack — but because each of its
rules, like each of yours, looks for
particular shapes: the SQL rules in it are
written for frameworks and query styles
this fixture does not use, and nobody put
a plain `eval()` rule in this particular
bundle.

Hold the two halves together, because
both are the lesson: a pack is a hundred
and fifty-one *somebody's judgements*
about what to look for. Borrowing them is
the fastest way to start scanning — and a
pack is a list, not a net. Chapter 13
returns to this.

## A second pack, aimed wider

```bash
semgrep scan --config p/security-audit --metrics=off fixtures/
```

`p/security-audit` is the registry's broad
security bundle, across languages.
Transcript `t05-registry-security-audit.txt`
records the shape of a bigger borrow:

```text
Ran 99 rules on 5 files: 4 findings.
```

225 rules were fetched; 99 applied to
these five files (77 Python, 20
JavaScript, 2 that work across languages)
— a pack spends only the rules that fit
the files in front of it. The findings:
the shell call again, the `eval()` the
Python pack had missed — and two findings
in `fixtures/suppressed.py`, at lines 12
*and* 16, the second of which will not
surprise you by chapter 8: line 16 carries
the lab's `nosemgrep` comment, and the
comment names the *lab's* rule, not this
one. Suppression is specific, and the
registry just proved it.

And the shell script in the same folder?
The security-audit pack — the run that
scanned it — flagged neither its
`curl … | bash` line nor its unquoted
`rm -rf`: of its 99 engaged rules, none
spoke bash. The lab's own six-rule file
remains the only thing in this guide that
caught the `rm`.

## The packs you did not run

The registry holds hundreds of packs —
per framework (Django, Flask, React…),
per purpose (secrets, correctness,
best-practice) — all used the same way:
`--config p/<name>`. Two cautions ride
along. A pack is downloaded at scan time,
so an offline machine scans with local
files only; keep copies of rules your
project depends on (a `--config` can just
as well name a folder you keep in the
repository). And borrowed rules deserve
the same reading as borrowed code: the
registry shows each rule's pattern on its
web pages (the Details links), and a pack
from the official registry is a different
trust decision than a YAML file from a
forum. Prefer the former.

## `--config auto`, and why the lab left it alone

One more config shape exists: `auto`,
which inspects your project and chooses
packs for its languages and frameworks by
itself. The lab did not run it, for a
reason the tool states plainly. With
metrics off — the lab's standing choice —
it refuses (transcript `t90-auto-needs-metrics.txt`):

```text
[ERROR]: Cannot create auto config when metrics are off.
Please allow metrics or run with a specific config.
```

Choosing packs requires phoning home;
named packs do not (beyond the download
itself). The guide's view: naming your
packs is the more predictable habit
anyway — you can say afterwards exactly
which rules ran, which is the difference
between a scan and a shrug.
