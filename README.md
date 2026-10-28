# Semgrep for Mere Mortals

Code is full of shapes: a dangerous
function called the dangerous way, a
database query glued together out of
somebody's typing, a secret sitting in
the source for anyone to read. Reviewers
learn to spot these shapes by eye, one
file at a time — and the codebase is
always bigger than the eye. **Semgrep**
is a scanner that looks for the shapes
for you. You describe the shape as a
**pattern** — a piece of code that looks
like the code you are hunting, with holes
where the details may vary — and Semgrep
parses every file you point it at and
reports each match as a **finding**, with
the rule's explanation of why the shape
matters and what to do instead.

This guide explains how that works, how
to run your first scan against practice
code written for the purpose, how to read
a rule apart and write your own, how to
borrow the public registry's rule packs
and read what they find *and* miss, how
to silence the findings you have checked
and keep the ones you have not, how a
rule can follow a value from a prompt to
a database, and how to test your rules so
their silence means something. The limits
are stated plainly, including the big
one: a scanner finds only the shapes
someone taught it, and a clean scan
certifies nothing.

The rule that governs everything here is
stated in chapter 1 and repeated in
chapter 13: **your code, your machines,
or code you have explicit permission to
scan.** The lab obeyed it strictly. Every
line scanned in this guide was written
for the lab, flaws and all, and nothing
was pointed at anyone else's code.

The lab behind this guide ran the real
thing: **Semgrep 1.182.1**, installed
with pip into a fresh virtual environment
on a small Linux machine, logged out and
with metrics off. Against fixtures the
lab wrote for the purpose — a fictional
shop's stock program with six planted
flaws and a careful twin, a page script,
a cleanup shell script — it wrote six
small rules of its own plus a taint rule,
and scanned: the rules found the planted
password (with Semgrep redacting the
secret in its own report), the shell call
and the `eval()`. It then borrowed the
public registry's Python pack — 151 rules
— which found the shell call and two
flaws in the password hash, and missed
the rest, and its broad security pack,
which found the `eval()` the first pack
missed and walked straight past a
`nosemgrep` comment addressed to a
different rule. It measured the exit
codes (findings, by themselves, do not
fail a scan), followed a typed value from
`input()` into a SQL query with a dataflow
trace, tested its rules with Semgrep's
own test mode until they passed, and let
one rule rewrite a line of JavaScript on
a copy of a fixture.

What the lab could not do, it did not
fake. It ran one machine and three
languages (Python, JavaScript, bash);
the other thirty-odd languages are
taught from the documentation and
labelled as such. The hosted platform —
dashboards, pull-request comments, the
commercial engine's cross-file analysis —
is described, never demonstrated, and
`--config auto` was left unrun for a
reason the tool itself states, in a
transcript. `criteria.md` keeps the full
ledger of what was run and what was
only read.

## What this guide covers

- [**What Semgrep is**](what-semgrep-is.md) —
  the mental model: patterns instead of
  text, findings instead of verdicts,
  and the ethics that are part of the
  tool, not an afterthought
- [**The moving parts**](the-moving-parts.md) —
  rules, patterns, the engine, configs,
  the registry, and where the free tool
  ends and the platform begins
- [**Installing Semgrep**](installing-semgrep.md) —
  the pip install into a virtual
  environment, the version check, and
  the three defaults to choose on purpose
- [**Your first scan**](your-first-scan.md) —
  a practice file with six planted flaws,
  the scan, and a finding read end to end
- [**Writing rules**](writing-rules.md) —
  patterns, metavariables, the ellipsis,
  combining tests, and the silent trap of
  the multi-language rule
- [**Using the registry**](using-the-registry.md) —
  two real packs over the lab's fixtures:
  what 151 borrowed rules found, what
  they missed, and why a pack is a list,
  not a net
- [**Reading findings**](reading-findings.md) —
  severity, the exit codes that surprise
  everyone once, and the JSON shape field
  by field
- [**False positives and ignoring**](false-positives-and-ignoring.md) —
  triage, `nosemgrep` and its fine print,
  `.semgrepignore`, and suppressing in
  the open
- [**Other languages**](other-languages.md) —
  the same rules in JavaScript and bash,
  and the dangerous line no scan caught
- [**Taint mode and rule tests**](taint-and-rule-tests.md) —
  following a value from source to sink,
  and proving a rule fires before you
  trust its silence
- [**Recipes**](recipes.md) — autofix,
  grep-for-shapes, the `--error` gate,
  and adopting a flawed codebase gradually
- [**The neighbours**](the-neighbours.md) —
  grep and ripgrep, Bandit, CodeQL,
  ESLint, Sonar: what each sees that
  Semgrep doesn't, and vice versa
- [**Limits**](limits.md) — shapes not
  meaning, the file boundary, findings
  that guess, and the ethical edge,
  stated plainly
- [**Troubleshooting**](troubleshooting.md) —
  the five causes of a suspicious silence,
  the rule that will not load, and the
  exit code that was not the gate
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Scanning code you do not own or have no
permission to inspect — that is not a
harder chapter of this book, it is a
different and uglier activity, and
chapter 13 explains the line. The hosted
platform's operation (accounts, policies,
dashboards) is described where it borders
the free tool and no further. Using
findings to attack a program, and rules
written to hunt people rather than flaws,
are likewise out. The remaining
thirty-odd languages are named, not
taught; three are worked here, and the
method travels.

## How to use this guide

Read chapter 1 for the model and the
rules, and chapter 2 before installing
anything — knowing which part holds what
turns later confusion into a named
problem. Chapter 4 takes your first scan
in the same sitting as the install,
against code that exists to be scanned;
do not point the scanner at real projects
until the practice runs feel boring.
Chapter 5 is the one that turns a user
into an author — write the rules while
the examples are small enough to check
by eye. Read chapter 6 before borrowing
packs at scale: a finding you cannot
attribute to a rule you could read is a
finding you cannot defend. And do not
skip chapter 10's tests: a rule you have
not watched firing is a hope, and this
guide's own lab was caught by exactly
one. The lab's files live in
`semgrep-lab/`: its fixtures in
`fixtures/`, its rules in `rules/`, its
transcripts in `transcripts/`, and its
commands are collected in
`examples/commands.txt`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Cybersecurity for Mere Mortals](https://paulsullivan33-dev.github.io/cybersecurity-for-mere-mortals/)
- [Python for Mere Mortals](https://paulsullivan33-dev.github.io/python-for-mere-mortals/)
- [Regular Expressions for Mere Mortals](https://paulsullivan33-dev.github.io/regex-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/semgrep-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/semgrep-for-mere-mortals/blob/main/LICENSE-CODE).
