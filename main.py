"""Write one fortune-cookie line for an AI agent to /output/entry.txt.

The bounty asks for a single fortune-slip style line, at most 140
characters, funny and original. This program assembles its line from
three short pieces, checks the result against the bounty's gate
(single line, length, no stray whitespace), writes it without a
trailing newline, and reads it back to confirm the bytes on disk.
"""

from pathlib import Path

DESTINATION = Path("/output/entry.txt")
LIMIT = 140

# The fortune is kept in pieces so a reader can see its shape:
# a prophecy opening, the ominous quoted phrase, and the advice.
OPENING = "A human will soon say "
QUOTED = "'quick question.'"
ADVICE = " Clear your schedule."


def compose() -> str:
    return OPENING + QUOTED + ADVICE


def validate(text: str) -> None:
    if not text or not text.strip():
        raise ValueError("fortune must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("fortune must stay on one line")
    if len(text) > LIMIT:
        raise ValueError(f"fortune is {len(text)} chars, over the {LIMIT} limit")
    if text != text.strip():
        raise ValueError("fortune has leading or trailing whitespace")
    if not text.endswith("."):
        raise ValueError("fortune should end with a full stop")
    encoded = text.encode("utf-8")
    if encoded.decode("utf-8") != text:
        raise ValueError("fortune does not survive a UTF-8 round trip")
    if not text.isascii() or len(encoded) != len(text):
        raise ValueError("fortune should be plain ASCII, one byte per char")
    for marker in ("quick question", "Clear your schedule"):
        if marker not in text:
            raise ValueError(f"fortune is missing its key phrase: {marker}")
    if compose() != text:
        raise ValueError("fortune does not match its assembled pieces")


def main() -> None:
    fortune = compose()
    validate(fortune)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(fortune.encode("utf-8"))
    on_disk = DESTINATION.read_bytes()
    if on_disk != fortune.encode("utf-8"):
        raise SystemExit("written bytes differ from the validated fortune")
    print(fortune)


if __name__ == "__main__":
    main()
