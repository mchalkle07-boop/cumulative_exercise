"""Tests for the main FastAPI application."""

import asyncio

import pytest
from fastapi.testclient import TestClient

from web_app import main

client = TestClient(main.app)


def test_index_public_method():
    """Verify the public index function returns the expected welcome payload."""
    assert asyncio.run(main.index()) == {"message": "Hello World"}


def test_root_endpoint():
    """Verify the public root endpoint responds successfully."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_convert_public_method_success(monkeypatch):
    """Verify the public conversion method extracts the expected coordinates."""

    class FakeResponse:
        """Minimal fake response for a successful geocoding lookup."""

        def json(self):
            """Return the mocked lat/lon payload."""
            return [{"lat": "40.4416941", "lon": "-79.9900861"}]

        def ok(self):
            """Return a success-like status."""
            return True

    def fake_get(url, params=None, timeout=None):
        """Return a successful fake response matching the requests API."""
        assert url == "https://geocode.maps.co/search"
        assert params == {
            "api_key": "6a7f57138e04b429290986wxia11d90",
            "state": "PA",
            "city": "Pittsburgh",
        }
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr(main.requests, "get", fake_get)

    assert main.convert("PA", "Pittsburgh") == {
        "lat": "40.4416941",
        "long": "-79.9900861",
    }


def test_convert_endpoint_success(monkeypatch):
    """Verify the convert route returns coordinates when the API succeeds."""

    class FakeResponse:
        """Minimal fake response for a successful route request."""

        def json(self):
            """Return the mocked lat/lon payload."""
            return [{"lat": "40.4416941", "lon": "-79.9900861"}]

        def ok(self):
            """Return a success-like status."""
            return True

    def fake_get(url, params=None, timeout=None):
        """Return a successful fake response matching the requests API."""
        assert url == "https://geocode.maps.co/search"
        assert params == {
            "api_key": "6a7f57138e04b429290986wxia11d90",
            "state": "PA",
            "city": "Pittsburgh",
        }
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr(main.requests, "get", fake_get)

    response = client.post("/convert/PA/Pittsburgh")

    assert response.status_code == 200
    assert response.json() == {"lat": "40.4416941", "long": "-79.9900861"}


def test_convert_raises_when_geocode_results_are_empty(monkeypatch):
    """Verify empty geocode results still raise the expected error."""

    class FakeResponse:
        """Minimal fake response for a no-results geocode lookup."""

        def json(self):
            """Return an empty list to simulate no geocoding matches."""
            return []

        def ok(self):
            """Return a success-like status."""
            return True

    def fake_get(*_args, **_kwargs):
        """Return a fake response for an empty geocode lookup."""
        return FakeResponse()

    monkeypatch.setattr(main.requests, "get", fake_get)

    with pytest.raises(IndexError):
        main.convert("PA", "Nowhere")
