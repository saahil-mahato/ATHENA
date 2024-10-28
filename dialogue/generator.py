import json
import google.generativeai as genai
from google.generativeai.protos import Schema
from google.generativeai.protos import Type
from dialogue import model


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


def generate_response(prompt: str) -> str:
    response = model.generate_content(
        contents=prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=schema
        ),
    )

    return json.loads(response.text)
