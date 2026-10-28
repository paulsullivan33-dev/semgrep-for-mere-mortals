# Troubleshooting

The failures this guide's lab actually
met, and the ones the lab's results make
predictable. Each entry is a symptom, a
cause, and the check that separates them.

## "It found nothing, and I don't believe it"

The most important symptom in the book,
because silence has five different causes
and four of them are the scanner's fault,
not the code's:

1. **The rules never ran on that file.**
   Read the scan status, not the findings:
   it says how many files were scanned and
   how many rules ran (`Ran 3 rules on 1
   file`). Rules apply per language — a
   Python rule spends nothing on a `.js`
   file — and a target that is a file the
   config's languages do not cover scans
   to a polite zero.
2. **The file was never scanned.** It may
   be listed in `.semgrepignore`, or (in a
   repository) `.gitignore`. The summary
   counts skips and names the reason;
   `--verbose` names the files (chapter 8).
3. **The line is suppressed.** A
   `nosemgrep` comment — yours, a
   predecessor's, a copied snippet's —
   silences its line. Search the file for
   the word.
4. **The rule is silently wrong.** The
   lab's exhibit: one rule listing
   `languages: [python, javascript]` found
   nothing in Python, forever, while its
   single-language twin fires (chapter 5).
   A pattern a shade too specific does the
   same. The check is chapter 10: scan a
   fixture you *know* is flawed. If the
   known flaw does not fire, the rule —
   not the code — is what you are debugging.
5. **The code is actually clean** — of
   the shapes in the rules you ran. This
   is the only cause that is good news,
   and chapters 9 and 13 explain why it
   still is not a certificate.

## "It found far too much"

A fresh pack over an old codebase can
return hundreds of findings. Do not
delete the pack and do not suppress
wholesale. Narrow in this order: read
three of the findings and ask whether the
rule is wrong for *this* codebase
(chapter 8's `paths:` scoping fits rules
that are right somewhere), whether one
shape needs a `pattern-not` for its safe
form (chapter 5), or whether the findings
are simply true and the work is real — in
which case chapter 11's diff-aware
adoption is the honest pace. Filtering by
`--severity WARNING` (or `ERROR`) trims a
report to one urgency band while you
triage; the lab used it in scratch to
confirm the WARNING password finding
drops out of an ERROR-only report.

## "The rule will not load"

A malformed pattern stops the scan before
it starts, loudly. The lab's deliberate
breakage (transcript `t91-broken-rule.txt`,
run in the lab's scratch folder):

```text
semgrep-core rule validation failed (PatternParseError)
[ERROR] Rule parse error in rule broken-rule:
 Invalid pattern for Python: Stdlib.Parsing.Parse_error
----- pattern -----
def ((( :
----- end pattern -----
```

and the exit code is **2** — the scan did
not run. Two things to take from the
capture: the error names the rule and
shows the offending pattern, so start
there; and the same output cheerfully
prints `✅ Scan completed successfully`
in its summary — trust the exit code and
the ERROR lines, never the smiley. YAML
indentation is the other load-time trap:
fields drifted out of alignment produce
rules that parse as different rules. When
in doubt, scan one tiny file with only
the suspect rule until it loads and fires
on a line written to trigger it.

## "The script says success but the scan found things"

Chapter 7's lesson from the other side:
without `--error`, findings exit 0 — the
command reports, it does not gate. If a
hook or CI step "passes" over findings,
this is why, nine times in ten. Add
`--error`, and re-check all three codes:
0 clean, 1 found, 2 broken.

## "The registry pack will not download"

Packs are fetched at scan time; an
offline machine, a blocked proxy or a
registry outage all stop the scan before
it starts. Local rule files never have
this problem — which is the practical
reason chapter 6 advises keeping copies
of the rules your project depends on, in
the project. If `--config p/…` fails and
a folder of the same rules exists
locally, `--config that-folder` is the
same scan with no network in it.

## "`--config auto` refuses to run"

Verbatim from the lab (transcript
`t90-auto-needs-metrics.txt`):

```text
[ERROR]: Cannot create auto config when metrics are off.
Please allow metrics or run with a specific config.
```

`auto` chooses packs by consulting
Semgrep's service, and it will not do so
with metrics off. The guide's answer is
chapter 6's: name your packs. If you
choose metrics and auto, know that the
choice was yours and what it bought.

## "The same finding appears twice"

Two rules in a pack can see one line two
ways — chapter 6's MD5 line was flagged
for being a weak hash and for being a
password hash, and both findings were
correct. Duplicates across *configs* are
the other common case: scanning with a
local file and a pack that contains a
cousin of the same rule. This is
bookkeeping, not malfunction; triage by
rule id (chapter 8 suppresses per rule,
which is exactly the granularity needed).
