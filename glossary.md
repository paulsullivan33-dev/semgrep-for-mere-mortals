# Glossary

**Autofix** — a rule's `fix:` template,
applied with `--autofix`, rewriting the
code a finding matched (chapter 11).

**Baseline** — a commit to compare
against (`--baseline-commit`), so only
findings on changed lines are reported;
documented-only in this guide
(chapter 11).

**check_id** — a finding's full rule
name in machine-readable output: the
config's prefix joined to the rule's
`id` (chapter 7).

**Config** — whatever `--config` names:
a rule file, a folder of rules, a
registry pack, a single registry rule,
or a URL (chapters 2 and 6).

**Ellipsis** — `...` in a pattern:
matches any arguments, any statements,
any code of the right grammatical kind
(chapter 5).

**False negative** — a real flaw no rule
matched. Invisible by definition; the
reason chapter 13 distrusts silence.

**False positive** — a finding whose
instance is not actually a problem.
Normal, expected, and handled by triage
(chapter 8).

**Finding** — one rule matching in one
place: rule id, file, lines, and the
rule's message (chapter 4).

**Generic mode** — Semgrep's
text-pattern matching for languages and
files without a grammar; documented-only
in this guide (chapter 9).

**Metavariable** — a `$NAME` in a
pattern: a hole standing for any one
piece of code; the same name twice must
match the same code (chapter 5).

**metavariable-regex** — a test applied
to the text a metavariable caught
(chapter 5).

**nosemgrep** — a comment that suppresses
findings on its line: named with a rule
id, it silences that rule only; bare, it
silences all of them (chapter 8).

**Pack** — a named, curated bundle of
rules in the registry: `p/python`,
`p/security-audit` (chapter 6).

**Pattern** — a piece of code with holes
in it, describing the shape a rule hunts
(chapters 2 and 5).

**pattern-not** — a pattern that
subtracts: the positive pattern must
match and this one must not (chapter 5).

**Registry** — the public rule library
at semgrep.dev, fetched from at scan
time (chapter 6).

**Rule** — one item in a rule file: an
`id`, languages, a severity, a message,
and a pattern or a taint definition
(chapter 2).

**Sanitizer** — in a taint rule, an
operation that makes a value safe on its
way from source to sink (chapter 10).

**SAST** — static application security
testing: analysing code without running
it. Semgrep is a SAST tool.

**Severity** — a rule's own judgement,
`ERROR`, `WARNING` or `INFO`, carried
into findings and JSON (chapters 5
and 7).

**Sink** — in a taint rule, a place
untrusted values must never reach: the
dangerous call (chapter 10).

**Source** — in a taint rule, a place
untrusted values enter: user input, a
request, a file (chapter 10).

**Syntax tree** — the grammatical
structure a parser builds from code;
what patterns match against (chapter 1).

**Taint mode** — a rule mode that
follows values from sources to sinks
instead of matching a shape (chapter 10).

**Triage** — reading a finding,
deciding whether its instance is a real
problem, and recording the decision
(chapter 8).
