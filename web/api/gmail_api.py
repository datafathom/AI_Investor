"""
==============================================================================
FILE: web/api/gmail_api.py
ROLE: Gmail API REST Endpoints (FastAPI)
PURPOSE: RESTful endpoints for sending emails via Gmail API and managing
         email preferences.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, Header, Query, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/gmail", tags=["Gmail"])


class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body_text: str
    body_html: Optional[str] = None
    access_token: Optional[str] = None


class SendTemplateRequest(BaseModel):
    to: str
    template_name: str
    template_context: Dict[str, Any] = {}
    access_token: Optional[str] = None


def _get_access_token(authorization: Optional[str], body_token: Optional[str]):
    """Helper to get access token from header or body."""
    if authorization and authorization.startswith('Bearer '):
        return authorization[7:]
    return body_token


@router.post("/send")
async def send_email(
    request: SendEmailRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: str = Header("demo-user")
):
    """Send email via Gmail API."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        
        if not access_token:
            raise HTTPException(status_code=401, detail="Missing Google access token")
        
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        result = await gmail_service.send_email(
            user_id=x_user_id,
            access_token=access_token,
            to=request.to,
            subject=request.subject,
            body_text=request.body_text,
            body_html=request.body_html
        )
        
        return {
            "success": True,
            "data": {
                "message_id": result.get("message_id"),
                "status": result.get("status"),
                "provider": result.get("provider")
            }
        }
    except HTTPException:
        raise
    except RuntimeError as e:
        if "quota" in str(e).lower():
            return JSONResponse(status_code=429, content={"success": False, "detail": str(e), "suggestion": "Use SendGrid fallback"})
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
    except Exception as e:
        logger.exception("Gmail send failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/send-template")
async def send_templated_email(
    request: SendTemplateRequest,
    authorization: Optional[str] = Header(None),
    x_user_id: str = Header("demo-user")
):
    """Send email using template."""
    try:
        access_token = _get_access_token(authorization, request.access_token)
        
        if not access_token:
            raise HTTPException(status_code=401, detail="Missing Google access token")
        
        # Render template
        from services.communication.email_templates import get_email_template_engine
        template_engine = get_email_template_engine()
        body_text, body_html = template_engine.render_template(
            template_name=request.template_name,
            context=request.template_context
        )
        
        subject = request.template_context.get('subject', f"Notification: {request.template_name}")
        
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        result = await gmail_service.send_email(
            user_id=x_user_id,
            access_token=access_token,
            to=request.to,
            subject=subject,
            body_text=body_text,
            body_html=body_html
        )
        
        return {
            "success": True,
            "data": {
                "message_id": result.get("message_id"),
                "status": result.get("status"),
                "provider": result.get("provider"),
                "template": request.template_name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Templated email send failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/preview")
async def preview_template(
    template_name: str = Query(...),
    context: str = Query("{}")
):
    """Preview email template without sending."""
    try:
        import json
        try:
            context_data = json.loads(context)
        except:
            context_data = {}
        
        from services.communication.email_templates import get_email_template_engine
        template_engine = get_email_template_engine()
        
        body_text, body_html = template_engine.render_template(
            template_name=template_name,
            context=context_data
        )
        
        return {
            "success": True,
            "data": {
                "template_name": template_name,
                "body_text": body_text,
                "body_html": body_html,
                "context": context_data
            }
        }
    except Exception as e:
        logger.exception("Template preview failed")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/stats")
async def get_stats(x_user_id: str = Header("demo-user")):
    """Get Gmail sending statistics for current user."""
    try:
        from services.communication.gmail_service import get_gmail_service
        gmail_service = get_gmail_service()
        
        stats = await gmail_service.get_send_statistics(x_user_id)
        return {"success": True, "data": stats}
    except Exception as e:
        logger.exception("Failed to get stats")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
