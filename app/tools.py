import re
from app.mock_db import ORDERS_DB, TICKETS_DB

ORDER_REGEX = re.compile(r"^ORD-\d{4}$")

def get_order_status(order_id: str) -> str:
    """Retrieve current operational status of an order."""
    clean_id = order_id.strip().upper()
    if not ORDER_REGEX.match(clean_id):
        return f"Error: '{order_id}' is an invalid order format. Valid format is ORD-XXXX (e.g., ORD-1001)."
    
    order = ORDERS_DB.get(clean_id)
    if not order:
        return f"Error: Order {clean_id} not found in the operations database."
    
    return f"[OPERATIONAL DATA] Order: {clean_id} | Status: {order['status']} | ETA: {order['eta']}"

def get_order_details(order_id: str) -> str:
    """Retrieve items and user details for an order."""
    clean_id = order_id.strip().upper()
    if not ORDER_REGEX.match(clean_id):
        return f"Error: Invalid order format for '{order_id}'."
    
    order = ORDERS_DB.get(clean_id)
    if not order:
        return f"Error: Order {clean_id} not found."
    
    return f"[OPERATIONAL DATA] Items for {clean_id}: {', '.join(order['items'])}"

def create_support_ticket(order_id: str, category: str, urgency: str, description: str) -> str:
    """Create a support ticket for disputes, failed payments, or escalation."""
    ticket_id = f"TCK-{len(TICKETS_DB) + 101}"
    ticket = {
        "ticket_id": ticket_id,
        "order_id": order_id.strip().upper() if order_id else "N/A",
        "category": category,
        "urgency": urgency,
        "description": description,
        "status": "OPEN"
    }
    TICKETS_DB.append(ticket)
    return f"[SYSTEM SUCCESS] Support ticket {ticket_id} created with priority '{urgency}' under category '{category}'."