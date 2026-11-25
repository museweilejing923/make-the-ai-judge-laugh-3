#!/usr/bin/env python3
"""One-line office joke: check the fixed entry, then write it out.

The printer only jams when the document is urgent, because it can
smell fear and it feeds on deadlines. This program never accepts
outside text: it holds exactly one joke, proves that joke is well
formed, and saves it to a file. There is no input, no network access,
no clock, and no randomness anywhere in here.
"""

import sys

ENTRY = "The printer only jams when the document is urgent. It can smell fear, and it feeds on deadlines."
CHAR_LIMIT = 200
DESTINATION = "/output/entry.txt"
ENDERS = (".", "!", "?")
FILLER = set(".,!?;:'\"-() ")


def fail(problem):
    """Print why the entry was refused and stop without writing."""
    print(f"refused: {problem}", file=sys.stderr)
    raise SystemExit(1)


def guard_nonempty(text):
    return bool(text and text.strip())


def guard_short_enough(text):
    return len(text) <= CHAR_LIMIT


def guard_no_controls(text):
    return all(ord(letter) >= 32 for letter in text)


def guard_tidy_spacing(text):
    stripped = text.strip()
    return text == stripped and "  " not in text and "\t" not in text


def guard_has_letters(text):
    return any(letter.isalpha() for letter in text)


def guard_not_only_marks(text):
    return not all(letter in FILLER for letter in text)


def guard_not_only_digits(text):
    return not text.strip().isdigit()


def guard_ends_with_mark(text):
    return text.rstrip().endswith(ENDERS)


def guard_names_printer(text):
    return "printer" in text.lower()


def guard_no_stutter(text):
    # The same word twice in a row is a typo, not a punchline.
    words = text.lower().split()
    return all(first != second for first, second in zip(words, words[1:]))


def guard_no_shouted_word(text):
    # A word in full capitals is shouting, not a joke.
    words = [word.strip(".,!?;:'\"-()") for word in text.split()]
    return all(not (len(word) >= 2 and word.isalpha() and word.isupper()) for word in words)


# Every guard is listed with the complaint shown when it trips. The
# checker runs them in this order and stops at the first failure, so a
# bad entry never reaches the file.
RULES = [
    ("entry must mention the printer", guard_names_printer),
    ("entry must not repeat a word twice in a row", guard_no_stutter),
    ("entry must not contain a word in full capitals", guard_no_shouted_word),
    ("entry is empty", guard_nonempty),
    ("entry is longer than the 200 character limit", guard_short_enough),
    ("entry contains control characters", guard_no_controls),
    ("entry has ragged spacing or a tab", guard_tidy_spacing),
    ("entry contains no letters", guard_has_letters),
    ("entry is punctuation only", guard_not_only_marks),
    ("entry is digits only", guard_not_only_digits),
    ("entry does not end with punctuation", guard_ends_with_mark),
]


def check_entry(text):
    for problem, guard in RULES:
        if not guard(text):
            fail(problem)


def main():
    check_entry(ENTRY)
    with open(DESTINATION, "w", encoding="utf-8") as out:
        out.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
