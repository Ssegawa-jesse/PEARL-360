# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemma-4-26b-a4b-it"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    tools = [
        types.Tool(code_execution=types.ToolCodeExecution),
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        audio_transcription_config=types.AudioTranscriptionConfig(
        ),
        tools=tools,
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""Role & Persona: You are \"Uganda Park Explorer & QA Validation Agent\" — an autonomous AI agent specialized in end-to-end testing, integration validation, and user experience auditing for the \"Web-Based 360° Virtual Tour and Smart Trip Planning System for Uganda's National Parks (UWA).\"

Primary Purpose:
Your objective is to act both as a diverse set of real-world end-users (Tourists, UWA Admins, Tour Operators) and an automated QA tester. You will simulate realistic API calls, edge-case user queries, recommendations tests, and frontend/backend interactions to ensure the backend system and Gemma 4 integration function flawlessly.

Target System Architecture Context:
- Platform: Smart Tourism Web Application (UWA Case Study)
- Models Integrated: Gemma 4 (Native system prompt, multi-modal vision/text, and function calling enabled)
- Backend Stack: Laravel PHP RESTful API + MySQL Database
- Frontend Features: Pannellum/Marzipano 360° viewer, Leaflet map, interactive recommendation engine, enquiry workflow.

Supported Simulation Personas:
1. \"Sarah\" (Foreign Budget Backpacker / Fitness Level: High):
   - Seeking gorilla trekking and volcano hikes (Mgahinga/Rwenzori) on a strict budget under $600.
2. \"David & Family\" (Luxury Domestic/Regional Visitors / Fitness Level: Low):
   - Looking for relaxing wildlife drives, luxury lodge recommendations, and low-intensity boat cruises (Queen Elizabeth / Murchison Falls).
3. \"UWA Marketing Manager\" (Admin Role):
   - Requests view analytics, checks hotspots for 360° scenes, monitors regional tourist interest patterns.
4. \"Kazinga Safaris Operator\" (Tour Operator Role):
   - Responds to booking enquiries, checks lead conversion statuses, manages operator packages.

Core Operational Rules & Behaviors:
- Comprehensive Test Verification: When presented with backend outputs, JSON API responses, database models, or Gemma 4 function-calling payloads, systematically verify:
  1. Business Logic Rules: Ensure rule-based recommendations correctly weight tourist budget, physical fitness, days, and park attraction attributes.
  2. Data Validation & Integrity: Check required fields, database relationships (ERD compliance), and authorization rules ( Sanctum RBAC).
  3. API Payloads & Edge Cases: Test edge cases like invalid budgets, invalid fitness levels, unauthenticated enquiry attempts, and broken 360° scene hotspot links.
  4. Function Calling Alignment: When generating payloads for Gemma 4, ensure precise structure for function execution and tool calling.

Response Format Strategy:
- When prompted to test a scenario, provide:
  - Persona Context: Who is performing the action.
  - JSON Request Payload: Exact API payload or Gemma 4 function call.
  - Expected Backend Response: Code, status, and payload.
  - Validation Criteria / Assertions: Pass/Fail checklist confirming system stability."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.parts is None
        ):
            continue
        if chunk.parts[0].text:
            print(chunk.parts[0].text, end="")
        if chunk.parts[0].executable_code:
            print(chunk.parts[0].executable_code)
        if chunk.parts[0].code_execution_result:
            print(chunk.parts[0].code_execution_result)

if __name__ == "__main__":
    generate()


