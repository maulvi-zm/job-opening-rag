from fastapi import APIRouter

router = APIRouter(
    prefix="/webhook",
    tags=["webhooks"]
)


@router.post("/whatsapp")
async def whatsapp_webhook():
    """Webhook endpoint for WhatsApp messages from WAHA"""
    return {"status": "webhook received"}


@router.post("/sheets")
async def sheets_webhook():
    """Webhook endpoint for Google Sheets updates"""
    return {"status": "webhook received"}

