# Your First Scan

Outcome of this chapter: you run a real
ruleset over a file with flaws planted in
it, and you can read one finding end to
end — what matched, where, and why the
rule cares. Everything later in the guide
is commentary on this one experience.

## The practice file

The lab's fixture is
`semgrep-lab/fixtures/shop.py`: forty-odd
lines pretending to be the stock program
of a fictional corner shop, written badly
on purpose. It contains six planted
mistakes:

1. a password written into the source
   (line 13),
2. a SQL query built by gluing a caller's
   text into the string (lines 18–19),
3. a caller's text typed at a prompt and
   glued into a query (lines 25–26),
4. a subprocess run through a shell
   (line 32),
5. a password hashed with MD5 (line 37),
6. and an `eval()` call (line 42).

The file also contains one blameless
function (`add`, line 45) so you can watch
the rules leave it alone. Its
companion `fixtures/clean.py` does the
same jobs the careful way. Both files are
in the repository; read `shop.py` before
scanning it, so the findings have something
to be checked against.

## The scan

From the `semgrep-lab` folder:

```bash
semgrep scan --config rules/lab-rules.yaml --metrics=off fixtures/shop.py
```

`--config` names the lab's own rule file
(chapter 5 takes it apart). The full
output is transcript
`semgrep-lab/transcripts/t01-first-scan.txt`;
the heart of it:

```text
Ran 3 rules on 1 file: 3 findings.

    fixtures/shop.py
    ❯❱ rules.lab-hardcoded-password
          ❰❰ Blocking ❱❱
          A password written into source code is shared with anyone
          who can read the code, and changing it means changing the
          program. Read secrets from the environment or a secrets
          store instead.

13┆ DB_PASSWORD=<redacted>
```

The scan status at the top is worth one
glance: six rules are in the file, but
only the three Python ones ran on a Python
file — rules travel with their languages,
and the JavaScript and bash rules waited
for chapter 9.

## Reading a finding

Each finding has the same anatomy:

- **The rule id** — `rules.lab-hardcoded-password`.
  The `rules.` prefix is the config's
  fingerprint (the rule file is named
  `lab-rules.yaml` inside `rules/`); the
  rest is the id the rule's author chose.
- **The message** — written by the rule's
  author, for this exact moment: what is
  wrong and what to do instead. A finding
  is only as helpful as its message.
- **The line** — file and line number,
  with the matched code printed.
- **Blocking** — the finding's weight.
  Semgrep presents findings as blocking:
  these are the ones a gate (chapter 11)
  would stop a release on — once you ask
  it to, which chapter 7's exit codes make
  precise.

One detail in the first finding deserves
its own sentence: the matched line reads
`DB_PASSWORD=<redacted>`. The fixture's
password is a made-up string
(`s3cret-shop-password`, printed in the
fixture for all to see), but Semgrep
redacts text that looks like a secret in
its own output — a small, correct instinct
in a tool whose reports get pasted into
tickets and chat windows.

The other two findings name line 32 (the
shell) and line 42 (the `eval()`). Check
them against the fixture and the anatomy
holds. Then notice what is *missing*: the
two glued queries (lines 18–19 and 26)
and the MD5 hash (line 37) drew no fire
from the lab's rules, because no lab rule
looks for those shapes. Hold that thought;
chapters 6, 10 and 13 each take a piece
of it.

## The clean file, and the check

Scan the careful version:

```bash
semgrep scan --config rules/lab-rules.yaml --metrics=off fixtures/clean.py
```

Silence: no findings, and the summary says
so (transcript `t12-clean-scan.txt`:
`Ran 3 rules on 1 file: 0 findings.`).
The parameterised query and the shell-free
subprocess call are exactly the shapes the
rules are *not* looking for.

Check: your scan of `shop.py` names lines
13, 32 and 42 and no others, and your scan
of `clean.py` names none. If your results
differ, chapter 14 is the map of what can
differ — but do not move on until these
two scans behave, because every later
chapter stands on them.
