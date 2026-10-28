# The Neighbours

Semgrep is one instrument in a crowded
drawer. This chapter characterises the
neighbours — what each sees that Semgrep
does not, and vice versa. The comparisons
are from the tools' documented designs,
not benchmarks run by this lab, and the
chapter says so rather than dressing
opinion as measurement.

## grep and ripgrep: letters, at great speed

`grep` (and its faster modern sibling
`ripgrep`) find *text*: the characters you
ask for, in any file, at remarkable speed.
For "which files mention this string at
all", nothing beats them, and this series
has a whole guide's worth of respect for
the text tools. What they cannot do is
grammar: `grep eval` finds the comment
that says "never use eval", the string
`"eval"`, and the function named
`evaluate` cut in half, and cannot tell
any of them from a call. Semgrep's pattern
is the same search with the grammar put
back — slower, fussier to write, and
answering the question you actually meant.
Reach for grep to find *words*; reach for
Semgrep to find *code*.

## Bandit: the Python-only specialist

Bandit is a security linter for Python
alone: install it, run it, and it applies
its built-in checks — shell calls, weak
hashes, hardcoded passwords, the same
fixture chapter 4 planted — with no
rule-writing at all. If your world is
only Python and you want the standard
checks with zero investment, Bandit is
the honest neighbour. Semgrep earns its
keep when you leave Python, or when the
check you need is *yours* — your
framework, your house rule, your pattern —
because Bandit's list is Bandit's, and
Semgrep's list is whoever's you load.

## CodeQL: the deep diver

GitHub's CodeQL builds a database of your
codebase and lets you query it — across
functions, across files, following data
the way chapter 10's taint mode does but
at whole-program depth. It answers
questions Semgrep's open-source engine
cannot: *can input from this HTTP handler
reach that query three calls later, in
another file?* The price is weight: a
database to build, a real query language
to learn, and runs measured in minutes
rather than seconds. The two are
complements more than rivals — Semgrep
for the fast, local, every-save checks;
CodeQL for the deep audit. (Semgrep's own
commercial engine, chapter 2, is the
vendor's answer in the same direction.)

## ESLint: the linter that lives in the toolchain

For JavaScript and TypeScript, ESLint is
already in most projects' build, checking
style and correctness, with security
plugins reaching toward Semgrep's ground.
Its rules are JavaScript code, written
against the parser's tree directly —
powerful, and a programming task rather
than a pattern. If your project is
JS-only and ESLint is already there, its
security plugins may cover you; Semgrep's
case is the multi-language project and
the rule you can write by showing it the
code you mean.

## SonarQube and the platforms

Sonar takes the platform road: a server,
dashboards, quality gates, history —
findings as an organisational process
rather than a command's output. For a
team that needs triage workflow and
trend lines, that weight is the point.
Semgrep's platform (chapter 2) plays in
the same space; the open-source engine
this guide teaches is the opposite bet —
no server, no state, a scan that lives
and dies in one command. Choose by
whether your problem is *findings* or
*managing findings*; this guide's readers
usually have the first problem.

## Compilers, type checkers, tests

A type checker (mypy, TypeScript's own)
proves whole classes of mistake absent —
wrong argument types, missing cases —
which no pattern can see, because those
mistakes are about *relationships*, not
shapes. Tests prove behaviour on the
cases they run. Semgrep proves something
narrower and different: that certain
shapes do or do not occur. A codebase
with all three is not three times
checked; it is checked along three
different axes, each blind where the
others see. The scanner's seat in the
drawer is earned, and it is not the
whole drawer.
