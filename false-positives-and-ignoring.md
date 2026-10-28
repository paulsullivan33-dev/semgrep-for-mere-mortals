# False Positives and Ignoring

Outcome of this chapter: a finding stops
being a nuisance to delete or a command to
obey, and becomes what it is — a claim you
check, with honest tools for recording
"I checked this one; here is my name on
it" when the claim is wrong.

## A finding is a claim, not a verdict

A rule says *this line has the shape I was
told to hunt*. It does not know — cannot
know, chapter 13 — whether this instance
is dangerous. The fixture's
`DB_PASSWORD` is a genuine problem. A test
file full of fake credentials, a string
that merely *looks* like the shape, a call
whose argument is a constant you control:
all are findings, and all are fine.
**Triage** — reading the line, deciding,
and recording the decision — is not a
failure of the tool. It is the tool's
normal operation, and the mechanisms in
this chapter exist to make the recording
cheap and visible.

## `nosemgrep`: the decision, written on the line

The lab's `fixtures/suppressed.py` holds
two identical `eval()` calls. One is bare.
The other carries a comment:

```python
return eval(expression)  # nosemgrep: lab-python-no-eval
```

Scan it with the lab's rules (transcript
`t06-nosemgrep.txt`): one finding, at line
12. Line 16 is passed over in silence.
The comment is a **suppression**: it names
a rule id, and for that line, that rule
does not fire. Three properties make it
the right shape for the job:

- **It is specific.** It names one rule.
  Chapter 6's registry scan is the proof
  by counterexample: the registry's own
  eval rule fired on line 16 anyway,
  because the comment names
  `lab-python-no-eval` and the registry's
  rule is called something else. A
  suppression silences exactly what it
  names — no more, which is what you want
  from an audit trail.
- **It lives with the code.** The next
  reader meets the decision at the line
  it concerns, not in a dashboard they
  may never open. (Write the *reason* in
  an ordinary comment beside it; the
  fixture's docstring models the habit.
  A bare, unexplained suppression is a
  smell of its own.)
- **It is per line, not per project.**
  The same rule keeps firing everywhere
  else.

A blunter instrument exists: a bare
`# nosemgrep`, with no rule named,
silences *every* rule on that line. The
lab verified it against the registry's
eval rule — the named version fired next
door, the bare version's line stayed
silent. Reach for it rarely: it also
silences the rule you have not met yet.

## Whole files: `.semgrepignore`

Some files should never be scanned at
all: generated code, vendored libraries,
test fixtures stuffed with deliberate
flaws (ahem). A `.semgrepignore` file at
the root of the scan lists path patterns
to skip, one per line, in the style of
`.gitignore`. The lab's demonstration is
self-contained in `semgrep-lab/ignore-demo/`:
a copy of the suppressed fixture, and a
`.semgrepignore` naming it. The scan
(transcript `t10-semgrepignore.txt`)
reports:

```text
 • Scan skipped:
   ◦ Files matching .semgrepignore patterns: 1
Ran 6 rules on 0 files: 0 findings.
```

Note that the skip is *reported*, not
silent: the summary counts what was
skipped and why, and `--verbose` names
the files. In a git repository Semgrep
also honours `.gitignore` by default —
documented behaviour the lab did not
exercise, since its checkout is not a
repository; between the two files, decide
deliberately what your scanner may not
see, because it cannot find flaws in code
it never reads.

## Scoping from the rule's side

A rule can also declare its own territory
with a `paths:` block — `include` and
`exclude` patterns the rule applies to.
The lab verified the shape in scratch:
the eval rule with `paths: exclude:
[bare.py]` over its only target reports
zero findings. This is the tool for rules
that are right *somewhere* — a web
framework's rule that should only look at
the routes folder — rather than a comment
sprinkled over fifty files.

## The discipline

Suppress in the open, by name, at the
line, with a reason. Ignore files by
listing them, where the listing is itself
reviewed. Never answer a noisy rule by
deleting the rule or abandoning the scan:
a rule that cries wolf on your codebase
is telling you something true about the
fit between the rule and the code, and
chapter 14's narrowing tools —
`pattern-not`, one more `patterns:` test —
usually fix the fit. The goal was never
zero findings. The goal is that every
finding left standing has been *decided*,
and every decision can be found.
