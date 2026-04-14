"""Tests for interactive CLI entry and flows."""

from types import SimpleNamespace

from click.testing import CliRunner

from super_pocket.cli import cli


def test_cli_without_arguments_prints_help_when_stdin_is_not_a_tty(monkeypatch):
    """Running `pocket` without arguments should print help in non-interactive mode."""

    rendered_output: list[str] = []

    monkeypatch.setattr("super_pocket.cli.sys.stdin", SimpleNamespace(isatty=lambda: False))
    monkeypatch.setattr(
        "super_pocket.cli.console.print",
        lambda message: rendered_output.append(str(message)),
    )

    result = CliRunner().invoke(cli, [])

    assert result.exit_code == 0
    assert rendered_output


def test_pocket_cmd_uses_spinner_and_help(monkeypatch):
    """Ensure interactive help path shows spinner and runs help command."""

    from super_pocket import interactive

    recorded: list[object] = []
    prompt_calls: list[str] = []

    monkeypatch.setattr(interactive.time, "sleep", lambda *_: None)
    monkeypatch.setattr(interactive, "display_logo", lambda: recorded.append("logo"))
    monkeypatch.setattr(
        interactive,
        "centered_spinner",
        lambda message, style="bold blue": recorded.append(("spinner", message)) or message,
    )

    class DummyLive:
        def __init__(self, spinner, refresh_per_second=None, transient=None):
            recorded.append(("live", spinner))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            recorded.append("live_exit")

    monkeypatch.setattr(interactive, "Live", DummyLive)

    def fake_prompt(message, **kwargs):
        prompt_calls.append(message)
        return next(prompt_values)

    monkeypatch.setattr(interactive, "Prompt", SimpleNamespace(ask=fake_prompt))
    monkeypatch.setattr(
        interactive,
        "subprocess",
        SimpleNamespace(run=lambda *args, **kwargs: recorded.append(("run", args[0]))),
    )

    prompt_values = iter(["help", "", "exit"])

    interactive.pocket_cmd()

    assert ("spinner", "Loading help...") in recorded
    assert ("run", ["pocket", "--help"]) in recorded
    assert any("Press" in msg or "Appuie" in msg for msg in prompt_calls)


def test_pocket_cmd_runs_iconify_flow(monkeypatch):
    """Ensure interactive iconify path builds the expected command."""

    from super_pocket import interactive

    recorded: list[object] = []
    prompt_calls: list[str] = []

    monkeypatch.setattr(interactive.time, "sleep", lambda *_: None)
    monkeypatch.setattr(interactive, "display_logo", lambda: recorded.append("logo"))
    monkeypatch.setattr(
        interactive,
        "centered_spinner",
        lambda message, style="bold blue": recorded.append(("spinner", message)) or message,
    )

    class DummyLive:
        def __init__(self, spinner, refresh_per_second=None, transient=None):
            recorded.append(("live", spinner))

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            recorded.append("live_exit")

    monkeypatch.setattr(interactive, "Live", DummyLive)

    def fake_prompt(message, **kwargs):
        prompt_calls.append(message)
        return next(prompt_values)

    monkeypatch.setattr(interactive, "Prompt", SimpleNamespace(ask=fake_prompt))
    monkeypatch.setattr(
        interactive,
        "subprocess",
        SimpleNamespace(run=lambda *args, **kwargs: recorded.append(("run", args[0]))),
    )

    prompt_values = iter([
        "iconify",
        "icon_raw.png",
        "icon_ios_squircle.png",
        "2048",
        "6.0",
        "",
        "exit",
    ])

    interactive.pocket_cmd()

    assert ("spinner", "Generating squircle icon...") in recorded
    assert (
        "run",
        [
            "pocket",
            "iconify",
            "-i",
            "icon_raw.png",
            "-o",
            "icon_ios_squircle.png",
            "--size",
            "2048",
            "--exponent",
            "6.0",
        ],
    ) in recorded
    assert any("iconify" in msg for msg in prompt_calls)
