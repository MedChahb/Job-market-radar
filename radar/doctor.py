"""Health checks for the local setup: the database and Ollama."""

from dataclasses import dataclass

import httpx
import psycopg


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _one_line(exc: Exception) -> str:
    return " ".join(str(exc).split())


def check_database(url: str) -> Check:
    """Connect to Postgres and confirm the pgvector extension is installed."""
    try:
        with psycopg.connect(url, connect_timeout=3) as conn:
            row = conn.execute(
                "select extversion from pg_extension where extname = 'vector'"
            ).fetchone()
    except psycopg.Error as exc:
        return Check("database", False, f"cannot connect: {_one_line(exc)}")
    if row is None:
        return Check("database", False, "connected, but the pgvector extension is missing")
    return Check("database", True, f"connected, pgvector {row[0]}")


def check_ollama(base_url: str) -> Check:
    """Confirm Ollama answers, and list the models already pulled."""
    try:
        version_response = httpx.get(f"{base_url}/api/version", timeout=3)
        version_response.raise_for_status()
        tags_response = httpx.get(f"{base_url}/api/tags", timeout=3)
        tags_response.raise_for_status()
        version = version_response.json()["version"]
        models = [model["name"] for model in tags_response.json().get("models", [])]
    except (httpx.HTTPError, KeyError, ValueError) as exc:
        return Check("ollama", False, f"not reachable at {base_url}: {_one_line(exc)}")
    pulled = ", ".join(models) if models else "no models pulled yet"
    return Check("ollama", True, f"version {version}, models: {pulled}")
