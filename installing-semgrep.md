# Installing Semgrep

Semgrep is written largely in Python (with
a fast OCaml engine doing the matching),
and the route this guide's lab used is the
Python one: pip, into a **virtual
environment** — a private folder holding
the program and its libraries, so the
install touches nothing else on the machine
and can be deleted by deleting the folder.
The project also publishes a Homebrew
package for macOS, standalone binaries,
and a Docker image; those are documented
routes the lab did not take, and they all
end at the same `semgrep` command.

## The pip install

You need a current Python 3. On a Debian
or Ubuntu machine:

```bash
sudo apt install python3 python3-venv
python3 -m venv ~/semgrep-venv
~/semgrep-venv/bin/pip install semgrep
~/semgrep-venv/bin/semgrep --version
```

On Windows and macOS the same pip route
works from a terminal with Python
installed; macOS readers may prefer
`brew install semgrep`, which lands at the
same place. In the venv route the command
lives in the venv's `bin` folder (`Scripts`
on Windows); either call it by its full
path, activate the environment first with
`source ~/semgrep-venv/bin/activate`, or —
as this guide's lab did — put the venv's
`bin` on your path while you work through
the chapters. Every command in the guide
is written as plain `semgrep`.

Check: the lab's version printout
(transcript `semgrep-lab/transcripts/t00-version.txt`)
is one line:

```text
$ semgrep --version
1.182.1
```

Version 1.182.1, on Python 3.12.3. The
version matters when you read other
people's advice: Semgrep releases roughly
every week, options occasionally move (the
autofix chapter's preview flag is spelled
`--dryrun` in this version, and the lab's
first attempt at `--dry-run` was refused
with a spelling suggestion), and every
transcript in this guide is from 1.182.1.

## What the first run does — and does not do

Unlike some tools in this series, Semgrep
creates no home folder, no daemon and no
account on first run. A scan is a single
pass over files you name, and then the
program exits. Three defaults are worth
knowing before chapter 4:

- **No login is needed** for local rules
  or for the public registry packs. The
  lab ran every scan in this guide logged
  out.
- **Metrics are on by default.** Semgrep
  sends anonymous usage statistics (which
  commands ran, which rules fired in
  aggregate). Every command in this guide
  adds `--metrics=off`, which the tool
  honours for everything except
  `--config auto` — that one feature
  refuses to run without metrics, as
  chapter 6 shows. Turn metrics off or
  leave them on, but choose on purpose.
- **Registry packs need the network.**
  Local rule files do not. Chapter 6 is
  where the difference first matters.

That is the whole install. There is no
service to start and nothing to configure:
the interesting artefact is not the
program but the rules, and chapter 4 is
already holding a file of them.
