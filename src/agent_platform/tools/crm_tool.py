import httpx
import os

CRM_READ_TOOL = {
    "name": "crm_get_contact",
    "description": "Get a CRM contact by tenant and contact ID",
    "input_schema": {
        "type": "object",
        "properties": {
            "tenant_id": {"type": "string"},
            "contact_id": {"type": "string"}
        },
        "required": ["tenant_id", "contact_id"]
    }
}


def crm_get_contact_handler(tenant_id: str, contact_id: str) -> str:
    base_url = os.getenv("CRM_READ_URL", "http://localhost:8081")
    try:
        resp = httpx.get(f"{base_url}/api/contacts/{tenant_id}/{contact_id}", timeout=5)
        return resp.text
    except Exception as e:
        return f"CRM lookup failed: {e}"
