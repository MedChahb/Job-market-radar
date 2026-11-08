import httpx
import respx

from radar.doctor import check_database, check_ollama

OLLAMA = "http://ollama.test"


@respx.mock
def test_ollama_ok_lists_models():
    respx.get(f"{OLLAMA}/api/version").mock(
        return_value=httpx.Response(200, json={"version": "0.34.4"})
    )
    respx.get(f"{OLLAMA}/api/tags").mock(
        return_value=httpx.Response(200, json={"models": [{"name": "qwen3:4b"}]})
    )

    check = check_ollama(OLLAMA)

    assert check.ok
    assert "0.34.4" in check.detail
    assert "qwen3:4b" in check.detail


@respx.mock
def test_ollama_ok_without_models():
    respx.get(f"{OLLAMA}/api/version").mock(
        return_value=httpx.Response(200, json={"version": "0.34.4"})
    )
    respx.get(f"{OLLAMA}/api/tags").mock(return_value=httpx.Response(200, json={"models": []}))

    check = check_ollama(OLLAMA)

    assert check.ok
    assert "no models pulled yet" in check.detail


@respx.mock
def test_ollama_unreachable():
    respx.get(f"{OLLAMA}/api/version").mock(side_effect=httpx.ConnectError("refused"))

    check = check_ollama(OLLAMA)

    assert not check.ok
    assert OLLAMA in check.detail


def test_database_unreachable_does_not_leak_password():
    check = check_database("postgresql://radar:secret-password@127.0.0.1:1/radar")

    assert not check.ok
    assert "secret-password" not in check.detail
