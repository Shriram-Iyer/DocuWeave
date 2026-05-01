"""
Integration test fixtures.
Requires docker-compose.test.yml to be running:
  docker compose -f docker-compose.test.yml up -d
"""
import os
import pytest

TEST_PG_URL = os.getenv("TEST_PG_URL", "postgresql+asyncpg://docuweave:docuweave@localhost:15432/docuweave_test")
TEST_MYSQL_URL = os.getenv("TEST_MYSQL_URL", "mysql+aiomysql://docuweave:docuweave@localhost:13306/docuweave_test")
TEST_MONGO_URL = os.getenv("TEST_MONGO_URL", "mongodb://docuweave:docuweave@localhost:27117/docuweave_test")
