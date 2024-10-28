"""
This module defines a function to generate a response from a generative AI model using JSON schema validation.

It imports necessary libraries, sets up a schema for the expected response format, and defines a function
to generate content based on a given prompt. The generated response is parsed from JSON format into a Python dictionary.

Modules:
- json: A built-in Python module for working with JSON data.
- google.generativeai: A library for interacting with Google's generative AI models.
- google.generativeai.protos: Contains protocol definitions for schema and type handling.
- dialogue: A custom module that provides access to the generative model.

Schema Definition:
The schema defines the structure of the expected response, which includes:
- response: A string containing the dialogue response.
- emotion: A string describing the emotion associated with the response.

Function:
- generate_response(prompt: str) -> dict:
    - Takes a string prompt as input.
    - Generates content using the model and specified configuration.
    - Returns the parsed JSON response as a Python dictionary.

Usage:
1. Ensure that the `dialogue` module is properly implemented and accessible.
2. Call `generate_response(prompt)` with your desired prompt to obtain a structured response.

Example:
    response = generate_response("What would an NPC say in a tavern?")
    print(response)  # Output will include 'response' and 'emotion' fields.
"""

import json
import google.generativeai as genai
from google.generativeai.protos import Schema
from google.generativeai.protos import Type
from dialogue import model

# Define the schema for the expected response
schema = Schema(
    type=Type.OBJECT,
    properties={
        "response": Schema(
            type=Type.STRING, description="The response of the dialogue."
        ),
        "emotion": Schema(type=Type.STRING, description="The emotion while saying it."),
    },
    required=["response", "emotion"],
)


def generate_response(prompt: str) -> dict:
    """
    Generate a response from the generative AI model based on the provided prompt.

    Args:
        prompt (str): The input prompt for which to generate a response.

    Returns:
        dict: A dictionary containing the generated 'response' and associated 'emotion'.
    """
    # Generate content using the model with specified generation configuration
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=schema
        ),
    )

    # Parse and return the JSON response as a Python dictionary
    return json.loads(response.text)
