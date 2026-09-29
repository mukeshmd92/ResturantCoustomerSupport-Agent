from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import os
from app.agent import execute_agent
from app.mock_db import ORDERS_DB, TICKETS_DB
from app.tools import get_order_status
from app.workflow import triage_complaint

app = FastAPI(title="AI Restaurant Support & Operations Agent", version="1.0.0")

class ChatRequest(BaseModel):
    message: str

class ComplaintRequest(BaseModel):
    complaint: str

@app.post("/api/agent/chat")
def chat_with_agent(req: ChatRequest):
    return execute_agent(req.message)

@app.get("/api/orders/{order_id}")
def api_order_details(order_id: str):
    clean_id = order_id.strip().upper()
    return ORDERS_DB.get(clean_id, {"error": "Order not found"})

@app.get("/api/orders/{order_id}/status")
def api_order_status(order_id: str):
    return {"status_info": get_order_status(order_id)}

@app.get("/api/support/tickets")
def api_list_tickets():
    return {"tickets": TICKETS_DB}
@app.post("/api/automation/triage")
def auto_triage(req: ComplaintRequest):
    """Automated complaint classification & triage workflow with structured output."""
    return triage_complaint(req.complaint)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()