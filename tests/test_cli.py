from typer.testing import CliRunner

from radar import __version__, cli
from radar.doctor import Check

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_doctor_passes_when_all_checks_pass(monkeypatch):
    monkeypatch.setattr(cli, "check_database", lambda url: Check("database", True, "up"))
    monkeypatch.setattr(cli, "check_ollama", lambda url: Check("ollama", True, "up"))

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 0
    assert "[ok  ] database: up" in result.output


def test_doctor_fails_when_a_check_fails(monkeypatch):
    monkeypatch.setattr(cli, "check_database", lambda url: Check("database", False, "down"))
    monkeypatch.setattr(cli, "check_ollama", lambda url: Check("ollama", True, "up"))

    result = runner.invoke(cli.app, ["doctor"])

    assert result.exit_code == 1
    assert "[FAIL] database: down" in result.output
