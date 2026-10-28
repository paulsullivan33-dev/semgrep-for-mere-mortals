# Writing Rules

Outcome of this chapter: you can read the
lab's rule file aloud, say what each piece
does, and write a rule of your own that
fires where you intend and nowhere else.
The file is `semgrep-lab/rules/lab-rules.yaml`:
six rules, each small enough to hold in
your head.

## The anatomy, on the smallest rule

```yaml
- id: lab-python-no-eval
  languages: [python]
  severity: ERROR
  message: >-
    eval() runs whatever text it is handed
    as code. Pass data to a parser or a
    lookup table instead, never to eval().
  pattern: eval(...)
```

Four fields do the administrative work.
The **id** names the rule in every finding.
**languages** says which files the rule
applies to — Semgrep will not waste it on
a JavaScript file, nor (chapter 4) run the
JavaScript rules on Python. **severity**
is one of `ERROR`, `WARNING` or `INFO`:
your judgement of how serious this shape
is, carried into the output and the JSON
(chapter 7). The **message** is the text a
future reader — quite possibly you, at a
tired moment — will actually read. Write
it for that reader: what is wrong, and
what to do instead.

The fifth field is the hunt itself:
**pattern**. `eval(...)` is a call to a
function named `eval`, and the **ellipsis**
(`...`) means *any arguments, or none, of
any shape*. Because the pattern is matched
against the syntax tree, all of these are
the same call to Semgrep: `eval(x)`,
`eval ( x )`, `eval(build(request))`, and
the call split across three lines. What
the pattern does not say, it does not
require: nothing here cares which function
the call sits in, or what the result is
assigned to.

## Metavariables: holes with names

The shell rule needs more aim:

```yaml
- id: lab-subprocess-shell-true
  ...
  pattern: subprocess.$FN(..., shell=True, ...)
```

`$FN` is a **metavariable**: a hole that
stands for any one piece of code of the
right grammatical kind — here, any function
name on the `subprocess` module, so `call`,
`run` and `Popen` are all caught by one
rule. The two ellipses say *other arguments
may come before and after*; the middle of
the pattern is the non-negotiable part:
`shell=True` must be present, spelled as
the constant `True`. A call that passes a
variable — `shell=use_shell` — does not
match, and that is correct behaviour for
this rule: the pattern claims only what
it can see.

The password rule needs two tests at once,
so it uses the plural form, **patterns** —
a list that must *all* hold:

```yaml
- id: lab-hardcoded-password
  ...
  patterns:
    - pattern: $NAME = $VALUE
    - metavariable-regex:
        metavariable: $NAME
        regex: '(?i).*(password|passwd|secret).*'
    - metavariable-regex:
        metavariable: $VALUE
        regex: '^".*"$'
```

Read it as a sentence: *find an assignment
of something to something, where the name
sounds like a password and the value is a
quoted string.* The first pattern binds
`$NAME` and `$VALUE`; each
**metavariable-regex** then tests the text
a metavariable caught. This is a guessing
rule — it keys on a name — and chapter 13
is honest that guessing rules guess. It
caught the fixture's `DB_PASSWORD` (and,
per chapter 4, Semgrep redacted the value
in its own report).

Two more shapes complete the file. The
JavaScript `innerHTML` rule uses
**pattern-not** to subtract the safe case:

```yaml
  patterns:
    - pattern: $EL.innerHTML = $DATA
    - pattern-not: $EL.innerHTML = "..."
```

*Assignment to innerHTML — but not when
the right-hand side is a constant string.*
`$EL` is the same metavariable in both
patterns, so the subtraction applies to
the very assignment the first pattern
caught. And the rule carries a sixth field,
**fix**, which proposes a rewrite —
`fix: $EL.textContent = $DATA` — using the
same metavariables the pattern bound.
Chapter 11 puts it to work. The bash
rule, last in the file, is the Python
rules' idea in another grammar:
`pattern: rm -rf $TARGET`, fired by
chapter 9's shell script.

And the twin of the first rule:
`lab-js-no-eval` is the same `eval(...)`
pattern with `languages: [javascript]`.
Two rules, one per language — which brings
us to the trap.

## The trap this lab fell into, so you don't

The lab's first version of this file had
*one* eval rule with
`languages: [python, javascript]`. It
looked reasonable. It was silently wrong:
on the Python fixture it found nothing at
all, while the Python-only rule fires on
the same line every time; a variant of the
pattern matched in JavaScript and still
not in Python. A rule that lists several
languages does not promise the same
behaviour in each, and the failure mode is
the worst kind — silence, which a busy
reader mistakes for "no problems here".

The guide's rules therefore take the
slightly longer road: **one rule per
language**, even when the pattern text is
identical. And the deeper lesson is
chapter 10's: a rule you have not tested
is a hope, not a check. Semgrep ships a
test mode for exactly this reason.

## Where rules live

A rule file is ordinary YAML and lives
where you keep ordinary project files —
the lab keeps its in `semgrep-lab/rules/`,
real projects usually keep a `.semgrep`
folder or pass files with `--config`. One
file may hold many rules (as `rules:` a
list), and `--config` accepts a folder to
load them all. YAML's one cruelty is
indentation: a rule whose fields drift
out of alignment simply stops meaning what
you wrote. When a rule will not load at
all, Semgrep says so loudly — chapter 14
has the error, captured.
