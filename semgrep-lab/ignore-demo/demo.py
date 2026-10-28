"""One finding the rules catch, and one they are told to skip.

The second eval() carries a nosemgrep comment naming the rule.
That line is this guide's stand-in for "a human looked at this,
decided it is safe here, and wrote down which rule they are
overruling". The lab's transcript shows the first line flagged
and the second one passed over in silence.
"""


def calculate(expression):
    return eval(expression)


def calculate_trusted(expression):
    return eval(expression)  # nosemgrep: lab-python-no-eval
