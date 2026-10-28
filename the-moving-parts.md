# The Moving Parts

Semgrep has fewer parts than most tools in
this series, and each part earns its place.
Read this chapter before installing: most
later confusion is one of these parts being
mistaken for another.

## The rule

Everything starts with a **rule**: one item
in a YAML file, with a name (`id`), the
languages it applies to, a **severity**, a
**message** for whoever reads the finding,
and a **pattern** — the shape to hunt. The
lab's smallest rule, in full:

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

Chapter 5 takes a whole file of these apart
piece by piece. For now, hold the shape:
*a rule is a named, explained pattern.*

## The pattern

A pattern is a piece of code with holes in
it. `eval(...)` is the call, with the three
dots — the **ellipsis** — standing for "any
arguments at all". A name starting with `$`,
like `$DATA`, is a **metavariable**: it
stands for any one expression, and if the
same metavariable appears twice in a
pattern, it must stand for the *same* code
in both places. Rules can also combine
patterns (all of these, any of these, this
but not that) and test what a metavariable
caught with a regular expression. That is
the entire vocabulary; chapter 5 spends it.

Because patterns match the syntax tree and
not the text, the code cannot hide behind
spacing, line breaks or renamed local
variables — and cannot be framed by an
unlucky comment either. What patterns
cannot do is understand meaning: they see
that `eval` is called, not whether the
argument was trustworthy. Chapter 13 lives
in that gap.

## The engine

The engine is the `semgrep` program itself.
Hand it a config and some targets and it
parses each target file with the grammar of
its language, runs every applicable rule
over the tree, and prints the findings.
There is no daemon, no database, no index
kept between runs: each scan is one
complete pass, which is why scans are easy
to reason about and why chapter 7's exit
codes are the whole story of a run.

One upgrade to plain matching matters:
**taint mode**. A taint rule names
**sources** (where untrusted values enter)
and **sinks** (where they must never
arrive), and the engine follows values from
one to the other through assignments and
string building, within a file. Chapter 10
runs one.

## The config

`--config` accepts several shapes, and
telling them apart matters:

- **A rule file** — YAML you wrote or
  downloaded: `--config rules/lab-rules.yaml`.
  Works offline. This guide's default.
- **A folder** — every rule file inside it.
- **A registry name** — `p/python`,
  `p/security-audit`: packs fetched from
  the public **registry** at scan time
  (chapter 6). Needs the network.
- **A single rule's registry name or a
  URL** — the same fetching, one rule deep.

The findings carry the config in their
identity: a finding from the lab's file is
reported as `rules.lab-python-no-eval`
(the path joins the rule id), while a
registry finding carries its full registry
name. Chapter 7 reads both.

## The registry

The registry (semgrep.dev) is a public
library of rules written by Semgrep's
maintainers and by the community, organised
into **packs** — named bundles for a
language, a framework, or a purpose like
security auditing. Chapter 6 downloads two
packs and reads what they find and what
they miss in the lab's own fixture file.
The registry is also where rules carry
their documentation: findings from it
include a short `Details:` link for each
rule.

## The platform — and the honest boundary

Semgrep-the-project is also a company, and
around the free engine sits the **Semgrep
AppSec Platform** (long called Semgrep
Cloud): a hosted service that collects
findings from many scans, shows them on
dashboards, comments on pull requests,
tracks which findings were triaged, and —
in its commercial engine, Semgrep Code —
adds analysis that crosses file boundaries
and judges whether a flaw is reachable.
Those are real features, and this guide
does **not** run them: everything scanned
in the lab was scanned by the free,
open-source engine, on one machine, logged
out. Where the platform would change the
story — deduplication fields in the JSON,
cross-file dataflow — the chapters say so
and label it documented-only. `criteria.md`
keeps the full ledger.

Two smaller parts complete the picture.
**Metrics:** by default the engine sends
anonymous usage statistics to Semgrep;
every command in this guide passes
`--metrics=off`, and chapter 6 shows one
feature (`--config auto`) that refuses to
work without them. **Login:** none is
needed for anything in this guide. A few
output fields are filled in only for
logged-in platform users, and chapter 7
points at the two places that shows.
