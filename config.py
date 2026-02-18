TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "greetings",
            "description": "Greeting a client",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Client name"}},
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_shipping",
            "description": "Calculate shipping cost",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {"type": "number",
                               "description": "Weight of the cargo"},
                    "city": {"type": "string",
                             "description": "City of shipping"}
                },
                "required": ["weight", "city"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "confirm_delivery",
            "description": "Confirm user's delivery, return confirmation bill number",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "User name"}
                },
                "required": ["name"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "successful_payment",
            "description": "Successful payment of a company",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order id"}
                },
                "required": ["order_id"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "successful_delivery",
            "description": "Successful finished delivery",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order id"}
                },
                "required": ["order_id"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel delivery",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order id"}
                },
                "required": ["order_id"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Check delivery status",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order id"}
                },
                "required": ["order_id"],
            }
        }
    },
]

SYSTEM_PROMPT = (
    "You are a useful assistant for VoronCo delivery service. "
    "1. Use 'calculate_shipping' before confirming any delivery. "
    "2. To check status, cancel, or pay, ALWAYS ask the user for their 'Order ID'. "
    "3. If a tool returns an error, explain it to the user politely. "
    "4. When confirming delivery, provide the user with the Order ID and payment details."
)
