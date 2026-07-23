from unittest.mock import patch
from fastapi.testclient import TestClient
from api import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))



client = TestClient(app)

@patch("Database.Postgres_DB.add_regex_rule")
def test_new_regex(mock_add):

    response = client.post(
        "/new-regex",
        json={
            "pattern": r"\bcasino\b"
        }
    )

    assert response.status_code == 200

    mock_add.assert_called_once_with(r"\bcasino\b")




@patch("Database.Postgres_DB.get_all_regex_rules")
def test_get_regexes(mock_get):

    mock_get.return_value = [
        {"id": 1, "pattern": r"\bcasino\b"},
        {"id": 2, "pattern": r"\bcrypto\b"}
    ]

    response = client.get("/get-regexes")

    assert response.status_code == 200

    assert response.json() == {
        "regex_rules": [
            {"id": 1, "pattern": r"\bcasino\b"},
            {"id": 2, "pattern": r"\bcrypto\b"}
        ]
    }

    mock_get.assert_called_once()