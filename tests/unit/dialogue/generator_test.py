"""
This module contains unit tests for the `generate_response` function from the `dialogue.generator` module.
It uses the `pytest` testing framework and `unittest.mock` to mock the behavior of the generative AI model's 
content generation method.

Modules:
- pytest: A framework for writing simple and scalable test cases.
- json: A built-in Python module for working with JSON data.
- unittest.mock: A module that allows you to replace parts of your system under test and make assertions about how they have been used.
- dialogue.generator: The module containing the `generate_response` function to be tested.

Fixtures:
- mock_generate_content: A pytest fixture that mocks the `generate_content` method of the `google.generativeai.GenerativeModel`.
  This allows for controlled testing without making actual API calls.

Tests:
- test_generate_response_keys: This test checks that the response from `generate_response` contains the expected keys (`response` and `emotion`) 
  and verifies that the response is structured correctly.

Usage:
1. Ensure that pytest is installed in your environment.
2. Run this script to execute the tests.

Example:
    To run the tests, execute this script directly or use the command line:
    $ pytest <script_name>.py
"""

import pytest
import json
from unittest.mock import patch
from dialogue.generator import generate_response


@pytest.fixture
def mock_generate_content():
    """Fixture to mock the generate_content method of GenerativeModel."""
    with patch("google.generativeai.GenerativeModel.generate_content") as mock:
        yield mock


def test_generate_response_keys(mock_generate_content):
    """Test that generate_response returns a dictionary with expected keys."""
    # Mocking the response from the model
    mock_response = json.dumps(
        {"response": "This is a test response.", "emotion": "happy"}
    )
    mock_generate_content.return_value.text = mock_response

    result = generate_response("What is your name?")

    # Assert that 'response' and 'emotion' keys are present in the result
    assert "response" in result
    assert "emotion" in result

    # Assert that the result contains exactly two keys
    assert len(result) == 2
