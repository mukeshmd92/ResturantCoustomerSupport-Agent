import os
import json
from pydantic import BaseModel, Field
from typing import Literal
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class TicketClassification(BaseModel):
    category: Literal["Payment", "Order", "Delivery", "Refund", "Technical"] = Field(
        ..., description="Root issue category"
    )
    urgency: Literal["Low", "Medium", "High"] = Field(
        ..., description="Calculated priority level"
    )
    summary: str = Field(..., description="1-sentence objective summary")
    action_required: str = Field(..., description="Actionable next step")

def triage_complaint(complaint_text: str) -> dict:
    prompt = f"""You are an automated restaurant triage system.
Analyze the customer complaint and classify it strictly.
Available Categories: Payment, Order, Delivery, Refund, Technical.
Urgency Rules:
- High: Payment deducted & order failed, severe delay > 45 mins, food safety.
- Medium: Wrong item delivered, cold food, cancellation dispute.
- Low: General inquiry, slow delivery within ETA.

Return ONLY a valid JSON object matching this schema:
{{
  "category": "...",
  "urgency": "...",
  "summary": "...",
  "action_required": "..."
}}

Customer Issue: "{complaint_text}"
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    parsed_json = json.loads(raw)
    validated = TicketClassification(**parsed_json)
    return validated.model_dump()