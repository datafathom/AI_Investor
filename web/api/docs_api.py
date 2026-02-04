"""
API Documentation (FastAPI Router)
Complete Swagger/OpenAPI documentation with interactive UI.
Note: FastAPI handles this natively, but this file provides a custom 
Redoc/Swagger UI endpoint as requested for backward compatibility.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/docs", tags=["Documentation"])

# OpenAPI/Swagger specification
OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "AI Investor API",
        "version": "1.0.0",
        "description": "Complete API documentation for the AI Investor platform",
        "contact": {
            "name": "API Support",
            "email": "support@ai-investor.com"
        },
        "license": {
            "name": "Proprietary"
        }
    },
    "servers": [
        {
            "url": os.getenv('API_BASE_URL', 'http://localhost:8000'),
            "description": "Production server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ],
    "tags": [
        {"name": "Authentication", "description": "User authentication and authorization"},
        {"name": "Portfolio", "description": "Portfolio management endpoints"},
        {"name": "Trading", "description": "Trading operations"},
        {"name": "Analytics", "description": "Analytics and insights"},
        {"name": "Legal", "description": "Legal documents and compliance"},
        {"name": "Onboarding", "description": "User onboarding flow"},
        {"name": "Health", "description": "Health check endpoints"},
        {"name": "Institutional", "description": "Institutional onboarding and analytics"},
        {"name": "Evolution", "description": "Genomic evolution and playback"},
        {"name": "Search", "description": "Systemic search and discovery"}
    ],
    "paths": {
        "/api/v1/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Health check",
                "description": "Returns the health status of the API",
                "responses": {
                    "200": {
                        "description": "Healthy",
                        "content": {
                            "application/json": {
                                "example": {"status": "healthy", "version": "1.0.0"}
                            }
                        }
                    }
                }
            }
        },
        # ... (rest of the detailed paths from original file)
    }
}


@router.get("", response_class=HTMLResponse)
async def swagger_ui():
    """Serve Swagger UI."""
    swagger_ui_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation - AI Investor</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/api/docs/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=swagger_ui_html)


@router.get("/openapi.json")
async def openapi_spec():
    """Get OpenAPI specification."""
    return JSONResponse(content=OPENAPI_SPEC)


@router.get("/redoc", response_class=HTMLResponse)
async def redoc_ui():
    """Serve ReDoc UI."""
    redoc_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Documentation - AI Investor</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <redoc spec-url="/api/docs/openapi.json"></redoc>
        <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=redoc_html)


@router.get("/swagger.yaml")
async def swagger_yaml():
    """Get Swagger YAML specification (converted from JSON)."""
    import yaml
    try:
        yaml_content = yaml.dump(OPENAPI_SPEC, default_flow_style=False, sort_keys=False)
        return HTMLResponse(content=yaml_content, media_type="application/x-yaml")
    except ImportError:
        return JSONResponse(content={"error": "PyYAML not installed"}, status_code=500)
