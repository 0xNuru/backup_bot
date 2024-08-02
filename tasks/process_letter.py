#!/usr/bin/env python3

from robocorp import vault, workitems
import json
import openai


def process_letter(text: str) -> json:
    openai_vault = vault.get_secret("OpenAI")
    openai.api_key = openai_vault["key"]
    prompt = "provide a valid json output containing the NHS number, Date of Birth, Patient name, Medication changes, Follow-up appointments, Diagnosis where available in the text suppled"
    json_schema = "{\n  \"NHS Number\": \"1234567890\",\n  \"Date of Birth\": \"17/08/1966\",\n  \"Patient Name\": \"Patricia Martins\",\n  \"Medication Changes\": {\n    \"Amlodipine\": \"increased to 10mg once daily\",\n    \"Sertraline\": \"increased to 50mg once daily\"\n  },\n  \"Follow-up_appointments\": {\n    \"Follow-up_in\": \"Dr Adedeji's Cardiology Clinic\",\n    \"Follow-up_date\": \"6 weeks time\"\n  },\n  \"Diagnosis\": \"acute heart failure\"\n}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type":"json_object"},
        messages=[
            {"role":"system","content":"Provide output in valid JSON. The schema of the json look like this: " + json.dumps(json_schema)},
            {"role":"user","content":f"{prompt} {text}"}
        ],
        temperature = 0.3
    )
    finish_reason = response.choices[0].finish_reason

    if (finish_reason == "stop"):
        summary = response.choices[0].message.content
        return summary
    else:
        error = {"error": "tokens exceeded"}
        return json.dumps(error)