# Taint Mode and Rule Tests

Outcome of this chapter: two upgrades to
everything so far. A rule that *follows a
value* instead of matching a shape, and a
way to *test* rules — because this guide
has already met one rule that failed
silently, and silence is the enemy.

## Taint: from shapes to journeys

Chapter 4's first fixture holds a worse
flaw than any shape in it: in `search()`,
text typed by a person at a prompt travels
into a SQL query (lines 25–26). A
shape-rule for it would have to guess how
the value is carried — a variable, a
concatenation, a helper. A **taint rule**
asks the real question: *can anything
from here reach there?*

The lab's taint rule is
`semgrep-lab/rules/taint-sql.yaml`:

```yaml
rules:
  - id: lab-taint-input-to-sql
    languages: [python]
    severity: ERROR
    message: >-
      Text typed by a user reaches a SQL query
      without being passed as a parameter. If
      the text contains a quote, it can change
      what the query means.
    mode: taint
    pattern-sources:
      - pattern: input(...)
    pattern-sinks:
      - patterns:
          - pattern-inside: |
              def $F(...):
                ...
          - pattern: $CURSOR.execute(...)
```

`mode: taint` changes what the engine
does with the rule. **pattern-sources**
names where untrusted values enter —
here, anything returned by `input()`.
**pattern-sinks** names where they must
never arrive — here, the argument of any
`execute()` call inside a function. (A
third list, **pattern-sanitizers**, names
operations that make a value safe on its
way; the lab's rule has none, because the
fixture performs none.) The engine then
follows values through assignments,
concatenations and returns, and reports
any complete journey.

Run it with `--dataflow-traces`
(transcript `t08-taint.txt`):

```text
Ran 1 rule on 1 file: 1 finding.

    fixtures/shop.py
    ❯❯❱ rules.lab-taint-input-to-sql
           26┆ cursor.execute("SELECT price FROM items WHERE name = '" + name + "'")

          Taint comes from:

           25┆ name = input("Item name: ")

          Taint flows through these intermediate variables:

           25┆ name = input("Item name: ")

                This is how taint reaches the sink:

           26┆ cursor.execute("SELECT price FROM items WHERE name = '" + name + "'")
```

The finding is the journey, printed: the
source line, the path, the sink. This is
the most honest output a scanner can
give — not merely *here is a bad shape*
but *here is the route your user's text
takes into your database*, checkable step
by step.

## What the taint rule did not say

It said nothing about `find_item`
(lines 16–20), whose query is also glued
— from its *parameter*. Correctly, by its
own lights: the rule's only source is
`input()`, and a parameter is not
`input()`. Whether parameters of web
handlers should count as sources is a
modelling decision — *your* decision,
written into the rule. Real rulesets
answer it with framework knowledge
(request objects in Flask or Django are
declared as sources). The lesson is the
mirror of chapter 9's: a taint rule sees
the journeys that begin at the sources it
was told about. Taint widens the eye; it
does not remove the need to aim it.

## Testing rules: making silence meaningful

Chapter 5's multi-language eval rule is
the cautionary tale: it matched nothing,
said nothing, and looked exactly like
success. Semgrep's answer is a test mode
for rules, driven by annotations in an
ordinary code file. The lab's test file,
`semgrep-lab/rules/lab-rules.test.py`:

```python
# ruleid: lab-python-no-eval
eval(user_text)

# ok: lab-python-no-eval
print(user_text)

# ruleid: lab-subprocess-shell-true
subprocess.call(cmd, shell=True)

# ok: lab-subprocess-shell-true
subprocess.call(["ls", "-l", path])
```

A `# ruleid: <id>` comment says *the next
line must be flagged by this rule*; an
`# ok: <id>` comment says *it must not*.
Run them (transcript `t09-rule-test.txt`):

```bash
semgrep --test --config rules/lab-rules.yaml rules/lab-rules.test.py
```

```text
2/2: ✓ All tests passed
```

Two rules under test, every expectation
met. Had the broken combined-language
rule been tested this way on day one, its
`ruleid` line would have failed loudly in
a test instead of silently in a scan —
which is the whole argument. A rule with
tests is a check; a rule without them is
a hope. Test yours before you scan
anything you care about, and add a test
line for every false positive you narrow
away in chapter 8, so the narrowing is
proven rather than remembered.
