# Reading Findings

Outcome of this chapter: a scan stops
being a screen of text and becomes data
you can act on — the JSON shape, field by
field, and the exit codes, which turn out
to say something subtler than "found" or
"not found".

## Severity, and the word "blocking"

Chapter 4's findings were all labelled
*Blocking*, including one whose rule said
`WARNING`. The severity lives in the rule
— `ERROR`, `WARNING`, `INFO` — and it is
the rule author's judgement, preserved
into the machine-readable output below.
The human output presents findings as
blocking because that is their default
destiny: left alone, they are what a gate
(chapter 11) stops on. Treat "blocking"
as *this finding wants a decision*, and
severity as the author's advice about how
urgent the decision is.

## The exit codes: a reporter, not a gate

Here is the fact about Semgrep that
surprises everyone once. Transcript
`semgrep-lab/transcripts/t02-exit-codes.txt`,
four runs:

```text
$ semgrep scan --config rules/lab-rules.yaml fixtures/shop.py
$ echo $?
0
$ semgrep scan --config rules/lab-rules.yaml --error fixtures/shop.py
$ echo $?
1
$ semgrep scan --config rules/lab-rules.yaml --error fixtures/clean.py
$ echo $?
0
$ semgrep scan --config rules/lab-rules.yaml --error fixtures/suppressed.py
$ echo $?
1
```

(Metrics and output redirections omitted
from the commands as printed here; the
transcript has them in full.)

Read it carefully: **three findings, and
the plain scan still exits 0.** `semgrep
scan` is a reporter — its exit code says
*the scan itself succeeded*. Findings are
its output, not its failure. The flag that
turns reporting into gating is `--error`:
with it, any finding makes the command
exit 1, and a clean scan still exits 0.

Everything about using Semgrep in scripts,
hooks and CI (chapter 11) hangs on this
distinction, and half of chapter 14's
troubleshooting is people meeting it from
the wrong side. A third code exists:
**exit 2** means the scan itself failed —
a rule that would not parse, a config that
would not load (chapter 14 has one,
captured). 0, 1 and 2: *ran clean*, *ran
and found*, *did not run* — but only when
you have asked with `--error` does 1 mean
"found"; without it, found and clean are
both 0.

## The JSON shape

For anything a program will read, there
is `--json`. Transcript `t03-json.txt`
pipes a scan through a few lines of Python
(the guide's lab notes keep the exact
commands); the summary it prints:

```text
top-level keys: ['engine_requested', 'errors', 'paths',
  'profiling_results', 'results', 'skipped_rules',
  'time', 'version']
rules.lab-hardcoded-password | fixtures/shop.py line 13 | severity: WARNING
rules.lab-subprocess-shell-true | fixtures/shop.py line 32 | severity: ERROR
rules.lab-python-no-eval | fixtures/shop.py line 42 | severity: ERROR
```

Everything a script needs lives in
`results`, one object per finding. The
first of them, in full:

```json
{
  "check_id": "rules.lab-hardcoded-password",
  "path": "fixtures/shop.py",
  "start": { "line": 13, "col": 1, "offset": 307 },
  "end":   { "line": 13, "col": 37, "offset": 343 },
  "extra": {
    "message": "A password written into source code ...",
    "metadata": {},
    "severity": "WARNING",
    "fingerprint": "requires login",
    "lines": "requires login",
    "validation_state": "NO_VALIDATOR",
    "engine_kind": "OSS"
  }
}
```

Field by field: `check_id` is the rule's
full name — the config's path prefix
joined to the id written in the rule file
(the bare id, without the prefix, is what
chapter 8's `nosemgrep` comments use).
`path`, `start` and
`end` locate the match to the column.
`extra.message` and `extra.severity` are
the rule's own words and judgement.
`engine_kind: OSS` is the free engine
signing its work.

Two fields say `requires login`:
`fingerprint` (a stable hash used to
recognise the same finding across scans)
and `lines` (the matched text). The
platform withholds them from anonymous
runs — a logged-in platform user gets
them filled. The finding is complete
without them: identity, place, message
and severity are all present. But it is
worth seeing the seam once, in print,
rather than discovering it in a pipeline:
this is exactly where the free tool ends
and the platform (chapter 2) begins.

## Other shapes of output

The same findings can be printed as
`--sarif` (the format security dashboards
and GitHub's code-scanning view consume),
`--emacs` or `--vim` (findings as editor
errors), or `--gitlab-sast`. The lab did
not run these — they are the JSON's
information in other envelopes, and this
guide labels them documented-only rather
than pretending otherwise. If your world
eats SARIF, the flag is there; everything
chapters 8 to 11 say about findings
applies unchanged.
