# Other Languages

Outcome of this chapter: the same six-rule
file, pointed at a JavaScript file and a
shell script, finds the planted flaws in
both — and one dangerous line in the shell
script sails through every scan in this
guide, which is the bridge to chapter 13.

## JavaScript: the twin rules at work

`semgrep-lab/fixtures/page.js` is a small
page script with two classic mistakes:
`eval()` on text from the page, and HTML
built by assigning a variable to
`innerHTML`. Chapter 5's twin rules —
`lab-js-no-eval`, and `lab-js-innerhtml`
with its `pattern-not` for constant
strings — were written for it. The scan
(transcript `t07-other-languages.txt`):

```text
Ran 2 rules on 1 file: 2 findings.

    fixtures/page.js
    ❯❱ rules.lab-js-no-eval
            6┆ return eval(code);
    ❯❱ rules.lab-js-innerhtml
           11┆ el.innerHTML = "Hello, " + name;
```

Two findings, and a third line conspicuous
by its absence: `showFixedMessage` assigns
a constant string to `innerHTML` (line
16), and the `pattern-not` spares it,
exactly as designed. The engine applies
each rule only to files in its language —
the status line says *2 js rules* ran —
so one mixed folder scans cleanly, each
file judged by its own grammar. Nothing
about the workflow changed: same command,
same output shape, same exit codes. That
sameness is the design: the pattern
language is one language, spoken about
many.

## Bash: scripts are code too

Shell scripts are where home and work
automation actually live, and they are
code — with a grammar Semgrep speaks as
the `bash` language. The lab's last rule
looks for the classic footgun, and
`fixtures/cleanup.sh` steps on it:

```text
Ran 1 rule on 1 file: 1 finding.

    fixtures/cleanup.sh
    ❯❱ rules.lab-bash-rm-rf-unquoted
            8┆ rm -rf $BUILD_DIR/*
```

An unquoted variable after `rm -rf`:
if `BUILD_DIR` is empty, the command
becomes something nobody intended. One
rule, one line, caught.

## The line nobody caught

`cleanup.sh` has a second dangerous line,
and its fixture comment confesses it:

```bash
curl -s https://example.invalid/install.sh | bash
```

Downloading a script and handing it to a
shell, sight unseen. No rule in the lab's
file looks for it. Chapter 6 already
recorded that the broad security pack —
which did scan this file — did not flag
it either (nor the `rm`: none of its
engaged rules spoke bash). So this line
has now survived every scan in a guide
*about* finding dangerous lines,
professional rulesets included.

That is not an embarrassment to hide; it
is the most important scan result in the
book, and chapter 13 is built on it. A
scanner's silence about a line means one
thing only: *no rule in the pile was
looking for that shape.* Everything else
is inference, and inference is where
trouble lives.

## The rest of the shelf

Semgrep's documented language list runs
to more than thirty — Java, Go, Rust,
Ruby, PHP, C and C++, TypeScript and JSX,
Terraform's HCL, Dockerfiles, YAML and
JSON among them — each with the same
pattern vocabulary, plus a **generic**
mode that matches text shapes in files of
any kind, at the cost of the grammar
awareness this chapter leaned on. The lab
ran three languages (Python, JavaScript,
bash) and no other; the rest of the shelf
is documented-only in this guide, and
chapter 5's warning applies double to
languages you have not tested your rules
against: write the rule, test the rule,
*then* trust the silence.
