# Recipes

Small jobs, each built only from machinery
the earlier chapters verified. Where a
recipe reaches past the lab — into a CI
service, say — the seam is labelled.

## Let the rule fix it: autofix

Chapter 5 gave the `innerHTML` rule a
`fix:` — a rewrite template written in the
pattern's own metavariables:

```yaml
    fix: $EL.textContent = $DATA
```

With `--autofix`, a scan stops reporting
and starts editing. The lab ran it on a
*copy* of the fixture (transcript
`t11-autofix.txt`) — run autofix on copies
or under version control until you trust
a rule's fix, because the editor is as
literal as the matcher:

```bash
cp fixtures/page.js fixtures/page-copy.js
semgrep scan --config rules/lab-rules.yaml --metrics=off --autofix fixtures/page-copy.js
```

```text
    ❯❱ rules.lab-js-innerhtml
           ▶▶┆ Autofix ▶ el.textContent = "Hello, " + name
           11┆ el.innerHTML = "Hello, " + name;
```

and afterwards:

```text
$ grep -n "textContent\|innerHTML" fixtures/page-copy.js
11:  el.textContent = "Hello, " + name;
16:  el.innerHTML = "Welcome back.";
```

Line 11 rewritten; line 16 — the constant
string the `pattern-not` excludes — left
alone, because a fix only ever applies
where its rule fires. Preview without
writing with `--autofix --dryrun` (the
spelling in 1.182.1 is `--dryrun`;
chapter 3 met its error message). The
registry's rules mostly offer no fix —
chapter 6's `Autofix ▶ False` — so the
fixes you get are usually from rules you
wrote, which is as it should be: a stranger's
rule may judge, but your own rules hold
the pen.

## grep, but for shapes

Every rule in this guide doubles as a
search tool. To answer *where in this
project do we ever start a shell?* over
code you own, one pattern and a folder
are the whole recipe:

```bash
semgrep scan --config rules/lab-rules.yaml --metrics=off path/to/project/
```

Folder targets scan recursively, each
file under its own language's rules —
chapter 6's five-file scan is the shape
of it. Add `--json` (chapter 7) when the
answer feeds another program, and
remember that a one-pattern throwaway
rule — written in a minute, deleted after
— is a legitimate use. Not every rule is
a policy; some are questions.

## The gate: scans that can say no

Chapter 7's lesson becomes a workflow:
a scan with `--error` exits 1 on findings,
which is exactly the contract a shell
hook or a CI step enforces. As a local
pre-commit habit:

```bash
semgrep scan --config rules/lab-rules.yaml --metrics=off --error .
```

Run by hand before committing, it is a
check; wired into a `pre-commit` hook or
a CI job — install Semgrep, run the same
command, let the exit code speak — it is
a gate. The lab verified the command and
its exit codes (transcript `t02`); the
wiring into any particular CI service is
documented-only here, and deliberately
small wherever you put it: the shorter
the gate's configuration, the less there
is to drift away from the command you
tested. Keep the rules in the repository,
so the gate and the code version together.

## Adopting a codebase that already has flaws

Point chapter 7's reporter at a large,
old project of yours and the first scan
may return hundreds of findings — most of
them in code nobody is touching. The
documented answer is **diff-aware
scanning**: `--baseline-commit <commit>`
reports only findings on lines changed
since that commit, so the gate guards new
code while the old findings are worked
through deliberately. The lab did not run
it — it needs a git repository, and the
lab's checkout is not one — so this
paragraph is labelled documented-only.
The principle needs no flag, though:
a scanner adopted gradually, with its
findings triaged (chapter 8) rather than
either ignored or treated as a stop-everything
alarm, is a scanner still running next year.
