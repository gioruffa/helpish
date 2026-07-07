"""helpish: list English words by length, handy for writing Pilish."""

from __future__ import annotations

from collections import defaultdict
from importlib.resources import files
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, Static
from wordfreq import zipf_frequency

WORDS_FILE = Path(str(files("helpish") / "words_alpha.txt"))


def load_words_by_length(path: Path) -> dict[int, list[str]]:
    """Read the word list once and bucket every word by its length."""
    buckets: dict[int, list[str]] = defaultdict(list)
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            word = line.strip()
            if word:
                buckets[len(word)].append(word)
    return buckets


class WordLengthApp(App[None]):
    """Type a number, see every English word of that length."""

    CSS = """
    #controls {
        height: auto;
        padding: 1 2;
    }

    #length-input {
        width: 20;
    }

    #summary {
        padding: 1 2;
        color: $text-muted;
    }

    #results {
        padding: 0 2;
    }
    """

    TITLE = "English Words by Length"
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.words_by_length: dict[int, list[str]] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="controls"):
            yield Label("Word length: ")
            yield Input(
                placeholder="enter a number",
                id="length-input",
                type="integer",
                restrict=r"\d*",
            )
            yield Label("  Contains: ")
            yield Input(
                placeholder="substring filter",
                id="filter-input",
            )
        yield Static("", id="summary")
        yield VerticalScroll(Static("", id="results"))
        yield Footer()

    def on_mount(self) -> None:
        if not WORDS_FILE.exists():
            self.query_one("#summary", Static).update(
                f"[red]Word list not found:[/] {WORDS_FILE}"
            )
            return
        self.words_by_length = load_words_by_length(WORDS_FILE)
        total = sum(len(w) for w in self.words_by_length.values())
        longest = max(self.words_by_length) if self.words_by_length else 0
        self.query_one("#summary", Static).update(
            f"Loaded {total:,} words (lengths 1–{longest}). "
            "Enter a number above."
        )
        self.query_one("#length-input", Input).focus()

    @on(Input.Changed, "#length-input")
    @on(Input.Changed, "#filter-input")
    def show_words(self) -> None:
        summary = self.query_one("#summary", Static)
        results = self.query_one("#results", Static)

        value = self.query_one("#length-input", Input).value.strip()
        needle = self.query_one("#filter-input", Input).value.strip().lower()
        if not value:
            summary.update("Enter a number above.")
            results.update("")
            return

        length = int(value)
        words = self.words_by_length.get(length, [])
        if needle:
            words = [word for word in words if needle in word]
        if not words:
            if needle:
                summary.update(
                    f"No words of length {length} containing '{needle}'."
                )
            else:
                summary.update(f"No words of length {length}.")
            results.update("")
            return

        ordered = sorted(
            words, key=lambda word: zipf_frequency(word, "en"), reverse=True
        )
        suffix = f" containing '{needle}'" if needle else ""
        summary.update(
            f"[b]{len(ordered):,}[/] words of length {length}{suffix} "
            "(most frequent first):"
        )
        results.update("  ".join(ordered))


def main() -> None:
    WordLengthApp().run()


if __name__ == "__main__":
    main()
