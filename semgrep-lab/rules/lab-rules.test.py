# Tests for the lab's Python rules (chapter 10). A "ruleid"
# comment says the next line must be flagged by that rule;
# an "ok" comment says it must not be.

# ruleid: lab-python-no-eval
eval(user_text)

# ok: lab-python-no-eval
print(user_text)

# ruleid: lab-subprocess-shell-true
subprocess.call(cmd, shell=True)

# ok: lab-subprocess-shell-true
subprocess.call(["ls", "-l", path])
