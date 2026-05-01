"""
Root test fixtures. Provides a FastAPI TestClient with template DB initialization bypassed.
"""
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch


@pytest.fixture(scope="session")
def client() -> TestClient:
    # Patch template DB init so tests don't need a real DB
    with (
        patch("docuweave.infrastructure.template_db_factory.init_template_db", new=AsyncMock()),
        patch("docuweave.infrastructure.template_db_factory.close_template_db", new=AsyncMock()),
    ):
        from docuweave.main import app
        with TestClient(app) as c:
            yield c
