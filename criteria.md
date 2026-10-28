# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's traffic is the lab talking to itself.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what the tool
   cannot do: patterns see shapes rather than meaning, the
   open-source engine's sight stops at the file boundary, a
   rule finds only the shape it was written to look for, a
   clean scan certifies nothing, and the legal and ethical
   edge around scanning code that is not yours.
8. **The ethics rule is in the text, early.** Chapter 1 and
   the README state the rule plainly — *your code, your
   machines, or explicit permission* — before any procedure
   depends on it, and later chapters point back to it where
   the tooling would make crossing the line easy: packs of
   other people's weakness-finding rules are one command away
   from any codebase on the machine.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7 GB Ubuntu 24.04 sandbox.
Semgrep **1.182.1** was installed with pip into a fresh virtual
environment (Python 3.12.3) and exercised against fixture code
written for this guide (`semgrep-lab/fixtures/`), scanned with
the lab's own rules (`semgrep-lab/rules/`) and with two packs
from the public registry. All transcripts live in
`semgrep-lab/transcripts/`. Every scan was run logged out,
with `--metrics=off`.

Run for real, with transcripts as evidence:

- Install and version (t00).
- The lab's six search rules over the planted-flaw fixture:
  three findings (hardcoded password — with the secret
  redacted by Semgrep itself in its own output — subprocess
  with `shell=True`, and `eval()`), and silence on the
  careful companion file (t01, t12).
- Exit codes, all four runs: findings with default flags
  exit 0; findings with `--error` exit 1; a clean file with
  `--error` exits 0; the partly suppressed fixture with
  `--error` still exits 1 on its one live finding (t02).
- `--json` output: the top-level keys, one summary line per
  finding, and the first finding's record in full, including
  the `fingerprint` and `lines` fields reading
  `requires login` for a logged-out run (t03).
- The public registry, which **was reachable** from the
  sandbox: `--config p/python` downloaded and ran 151 rules
  over two files (3 findings — the shell call and two MD5
  rules; the glued SQL, the `eval()` and the plaintext
  password in the same file were not flagged by this pack),
  and `--config p/security-audit` fetched 225 rules of which
  99 engaged with the five fixture files (4 findings: the
  shell call, and `eval-detected` in both Python fixtures —
  including the line carrying a `nosemgrep` comment that
  names the lab's rule, not the registry's) (t04, t05).
- Suppression: the lab rules over `fixtures/suppressed.py`
  report only the uncommented `eval()`; the named comment
  silences its own line for its own rule (t06).
- Other languages: the JavaScript fixture (the `eval()` and
  the variable `innerHTML` findings, with the constant-string
  assignment spared by `pattern-not`) and the bash fixture
  (the unquoted `rm -rf` finding; the fixture's
  `curl … | bash` line flagged by no scan in the guide)
  (t07).
- Taint mode with `--dataflow-traces`: the
  `input()` → `execute()` journey in the fixture reported
  with its source, path and sink (t08).
- Rule tests: `semgrep --test` over the annotated test file
  — "2/2: ✓ All tests passed" (t09).
- `.semgrepignore`: the ignore-demo scan reports the skip in
  its summary and scans 0 files (t10).
- Autofix: the `innerHTML` rule's `fix:` applied to a copy
  of the fixture rewrote the variable assignment and left
  the constant one standing (t11).
- A deliberately broken rule: the scan stops with a
  `PatternParseError` naming the rule and the pattern, and
  exits 2 — while its summary prints a success line (t91;
  the broken rule itself was kept in the lab's scratch
  folder, out of this repository).

Also run for real, in the lab's scratch folder and not kept
as transcripts (the results shaped the guide's rules and
text): a single rule listing `languages: [python, javascript]`
with the pattern `eval(...)` found **nothing** in the Python
fixture where the Python-only rule fires, and a metavariable
variant of it matched in JavaScript only — the reason the
shipped rules are one-per-language (chapter 5); a bare
`# nosemgrep` silenced every rule on its line, including the
registry's; a rule carrying `paths: exclude:` for its only
target reported zero findings; the `--severity` filter was
confirmed to select exactly one severity band; and
`--autofix --dryrun` previewed the chapter 11 rewrite
without writing it.

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- The Semgrep AppSec Platform (dashboards, pull-request
  comments, triage tracking) and the commercial Semgrep Code
  engine's cross-file dataflow and reachability analysis.
  Everything scanned here was scanned by the free OSS engine.
- `--config auto` and the packs it would choose: with metrics
  off it refuses to run (the refusal itself is transcript
  t90), and the lab did not run it with metrics on.
- `semgrep ci` as wired into a hosted CI service; chapter 11
  verifies the scan command and its exit codes locally and
  labels the wiring documented.
- `--baseline-commit` diff-aware scanning, which needs a git
  repository; the lab's checkout is not one.
- The SARIF, Emacs, Vim and GitLab output formats.
- Generic mode, and every supported language beyond the
  three the lab scanned (Python, JavaScript, bash).
- `.gitignore` handling in a real repository.
- The comparison tools in chapter 12 are characterised, not
  benchmarked.

Fixtures are this guide's own and deliberately generic: a
fictional corner shop's stock program with six planted flaws
and a careful twin, a small page script, a cleanup shell
script with a confessed second flaw, and a suppression
demonstration. No example is modelled on any real person,
codebase, service or organisation, and nothing was scanned
that the lab did not itself write.
