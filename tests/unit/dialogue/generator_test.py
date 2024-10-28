import pytest
import json
from unittest.mock import patch
from dialogue.generator import generate_response


@pytest.fixture
def mock_generate_content():
    with patch("google.generativeai.GenerativeModel.generate_content") as mock:
        yield mock


def test_generate_response_keys(mock_generate_content):
    # Mocking the response from the model
    mock_response = json.dumps(
        {"response": "This is a test response.", "emotion": "happy"}
    )
    mock_generate_content.return_value.text = mock_response

    result = generate_response("What is your name?")

    assert "response" in result
    assert "emotion" in result

    assert len(result) == 2


if __name__ == "__main__":
    pytest.main()
